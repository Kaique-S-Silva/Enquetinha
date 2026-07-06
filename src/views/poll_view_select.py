import discord

from src.utils.formatting import emoji_slash
from src.utils.embed import update_embed
from src.database.connection import get_vote_counts, register_vote, close_poll_db

class PollView(discord.ui.View):
    def __init__(self,
               options: list[str], poll_id: int, options_id: dict[str, int],
               time: float | None):
        super().__init__(timeout=time)

        self.poll_id = poll_id
        self.options_id = options_id
        self.options = options
        self.numbers = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣"]

        self.message: discord.InteractionMessage | discord.Message | None = None

        menu_options = []
        for index, option in enumerate(options):
            menu_options.append(
                discord.SelectOption(
                    label=option,
                    value=str(index),
                    emoji=self.numbers[index]
                )
            )

        self.select = discord.ui.Select(
            placeholder="Selecione uma opção para votar",
            min_values=1,
            max_values=1,
            options=menu_options,
            custom_id="select_vote"
        )

        self.select.callback = self.select_clicked

        self.add_item(self.select)

        close_button = discord.ui.Button(
            label="Encerrar enquete",
            style=discord.ButtonStyle.danger,
            custom_id="close_poll"
        )

        close_button.callback = self.button_close_poll
        self.add_item(close_button)
    
    async def select_clicked(self, interaction: discord.Interaction):
        if not interaction.message: return

        choose_value = self.select.values[0]
        voted_option = self.options[int(choose_value)]

        await register_vote(self.poll_id, self.options_id[voted_option], interaction.user.id)
        counts = await get_vote_counts(self.poll_id)

        embed = update_embed(
            embed=interaction.message.embeds[0],
            counts=counts
            )
        
        await interaction.response.edit_message(embed=embed)
        await interaction.followup.send(f"Voto registrado em **{voted_option}**", ephemeral=True)
    
    async def button_close_poll(self, interaction: discord.Interaction) -> None:
        is_admin = False

        if isinstance(interaction.user, discord.Member): # Caso ocorra o uso na DM, o retorno seria discord.User
            is_admin = interaction.user.guild_permissions.manage_messages
        
        if not is_admin: # Caso não seja da moderação
            await interaction.response.send_message("Você não tem permissão", ephemeral=True)

        await self.close_poll(interaction=interaction)
        self.stop()
    
    async def on_timeout(self) -> None:
        await self.close_poll(None)
    
    async def close_poll(self, interaction: discord.Interaction | None = None):

        for item in self.children:
            if isinstance(item, (discord.ui.Button, discord.ui.Select)):
                item.disabled = True
        
        embed: discord.Embed | None = None

        if interaction and interaction.message:
            embed = interaction.message.embeds[0]
        elif self.message:
            embed = self.message.embeds[0]
        if embed is None: 
            return
        
        counts = await get_vote_counts(self.poll_id)

        end_embed = update_embed(embed=embed, counts=counts, end=True)

        if interaction:
            await interaction.response.edit_message(embed=end_embed, view=self)
        elif self.message:
            try:
                await self.message.edit(embed=end_embed, view=self)
            except discord.HTTPException:
                pass
        
        await close_poll_db(self.poll_id)

        