import discord
from discord import app_commands
from discord.ext import commands

import src.database.connection as sql

class Poll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="poll", description="Cria a enquete")
    @app_commands.describe(pergunta="Pergunta da enquete", 
                           opcao1="Opção obrigatória", opcao2="Opção obrigatória", 
                           opcao3="Opção nao obrigatória", opcao4="Opção nao obrigatória", opcao5="Opção nao obrigatória",
                           tempo="Quantidade de tempo da enquete")
    async def poll(self, interaction: discord.Interaction, 
                   pergunta: str, 
                   opcao1: str, opcao2: str, 
                   opcao3: str | None = None, opcao4: str | None = None, opcao5: str | None = None,
                   tempo: float | None = None):
        options = [opcao1, opcao2, opcao3, opcao4, opcao5]
        optionsNotNone = [op for op in options if op is not None]

        if not interaction.guild_id:
            return
        poll_id, options_id = await sql.create_poll(pergunta, optionsNotNone, interaction.user.id, interaction.guild_id)

        pollview = PollView(optionsNotNone, poll_id, options_id, tempo)

        embed = discord.Embed(
            title=pergunta,
            description="Vote usando os botões abaixo!",
            color=discord.Color.blurple()
        )

        for field in optionsNotNone:
            embed.add_field(name=field, value="0 votos", inline=False)

        embed.set_footer(text="Cada pessoa pode votar apenas uma vez.")

        await interaction.response.send_message(embed=embed, view=pollview)

        pollview.message = await interaction.original_response()

        
class PollView(discord.ui.View):
    def __init__(self, opcoes: list[str], poll_id: int, options_id: dict[str, int], time: float | None):
        super().__init__(timeout=time)
        self.poll_id = poll_id
        self.options_id = options_id
        self.opcoes = opcoes

        self.message: discord.InteractionMessage | discord.Message | None = None
        for indice, opcao in enumerate(opcoes):
            button = discord.ui.Button(
                label=opcao,
                style=discord.ButtonStyle.primary,
                custom_id=str(indice)
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


        for index, option in enumerate(embed.fields):
            if not option.name:
                continue

            votos = counts.get(option.name)
            if votos is None:
                votos = 0
            
            embed.set_field_at(
                index=index,
                name=option.name,
                value=f"{votos} votos",
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

        for index, option in enumerate(embed.fields):
            if not option.name:
                continue

            votes = counts.get(option.name, 0)

            embed.set_field_at(
                index=index,
                name=option.name,
                value=f"{votes} votos",
                inline=option.inline
            )

        if interaction:
            await interaction.response.edit_message(embed=embed, view=self)
        elif self.message:
            try:
                await self.message.edit(embed=embed, view=self)
            except discord.HTTPException:
                pass
        
        await sql.close_poll_db(self.poll_id)

    
async def setup(bot: commands.Bot):
    await bot.add_cog(Poll(bot))