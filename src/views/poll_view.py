import discord

import src.database.connection as sql
from src.utils.formatting import emoji_slash
from src.utils.embed import update_embed

class PollView(discord.ui.View):
    def __init__(self, opcoes: list[str], poll_id: int, options_id: dict[str, int], time: float | None):
        super().__init__(timeout=time)
        self.poll_id = poll_id
        self.options_id = options_id
        self.opcoes = opcoes
        self.numbers = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣"]

        self.message: discord.InteractionMessage | discord.Message | None = None
        for indice, opcao in enumerate(opcoes):
            button = discord.ui.Button(
                label=opcao,
                style=discord.ButtonStyle.success,
                custom_id=str(indice),
                emoji=self.numbers[indice]
            )

            button.callback = self.clicked
            self.add_item(button)
        
        close_button = discord.ui.Button(
            label="Encerrar enquete",
            style=discord.ButtonStyle.danger,
            custom_id="btn_encerrar_enquete"
        )

        close_button.callback = self.button_close_poll
        self.add_item(close_button)


    async def clicked(self, interaction: discord.Interaction):
        
        if interaction.data is None: # pylance trouble
            return
        custom_id = interaction.data.get("custom_id")

        if custom_id is None: # pylance trouble
            return
        
        voted_option = self.opcoes[int(custom_id)]
            

        if interaction.message is None: # pylance trouble
            return

        await sql.register_vote(self.poll_id, self.options_id[voted_option], interaction.user.id)

        embed = interaction.message.embeds[0]

        counts = await sql.get_vote_counts(self.poll_id)
        embed = update_embed(embed=embed, counts=counts)
        total = sum(counts.values())


        for index, option in enumerate(embed.fields):
            if not option.name:
                continue

            votes = counts.get(option.name, 0)
            
            embed.set_field_at(
                index=index,
                name=option.name,
                value=f"{emoji_slash(votes, total)} {votes} votos",
                inline=option.inline
                )
        await interaction.response.edit_message(embed=embed)
        await interaction.followup.send("Voto registrado", ephemeral=True)
    
    async def button_close_poll(self, interaction: discord.Interaction):
        is_admin = False
        if isinstance(interaction.user, discord.Member):
            is_admin = interaction.user.guild_permissions.manage_messages

        if not is_admin:
            await interaction.response.send_message("Você não tem permissão para encerrar a enquete", ephemeral=True)
            return
        
        await self.close_poll(interaction=interaction)
        self.stop()


    async def on_timeout(self) -> None:
        await self.close_poll(None)
    
    async def close_poll(self, interaction: discord.Interaction | None = None):
        for item in self.children:
            if isinstance(item, discord.ui.Button):
                item.disabled = True    

        embed: discord.Embed | None = None

        if interaction and interaction.message:
            embed = interaction.message.embeds[0]
        elif self.message:
            embed = self.message.embeds[0]

        if embed is None:
            return

        embed.description = f"Enquete encerrada"
        embed.color = discord.Color.red()

        counts = await sql.get_vote_counts(poll_id=self.poll_id)
        total = sum(counts.values())

        for index, option in enumerate(embed.fields):
            if not option.name:
                continue

            votes = counts.get(option.name, 0)

            embed = update_embed(embed, counts)

        if total > 0:
            max_votos = max(counts.values())
            winners = [name for name, votos in counts.items() if votos == max_votos]
            embed.add_field(
                name="🏆 Vencedor: ",
                value=", ".join(winners),
                inline=False
            )

        if interaction:
            await interaction.response.edit_message(embed=embed, view=self)
        elif self.message:
            try:
                await self.message.edit(embed=embed, view=self)
            except discord.HTTPException:
                pass
        
        await sql.close_poll_db(self.poll_id)