import discord
from discord import app_commands
from discord.ext import commands

class Poll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="poll", description="Cria a enquete")
    @app_commands.describe(pergunta="Pergunta da enquete", 
                           opcao1="Opção obrigatória", opcao2="Opção obrigatória", 
                           opcao3="Opção nao obrigatória", opcao4="Opção nao obrigatória", opcao5="Opção nao obrigatória")
    async def poll(self, interaction: discord.Interaction, 
                   pergunta: str, 
                   opcao1: str, opcao2: str, 
                   opcao3: str | None = None, opcao4: str | None = None, opcao5: str | None = None):
        options = [opcao1, opcao2, opcao3, opcao4, opcao5]
        optionsNotNone = [op for op in options if op is not None]

        pollview = PollView(optionsNotNone)

        embed = discord.Embed(
            title=pergunta,
            description="Vote usando os botões abaixo!",
            color=discord.Color.blurple()
        )

        for field in optionsNotNone:
            embed.add_field(name=field, value="0 votos", inline=False)

        embed.set_footer(text="Cada pessoa pode votar apenas uma vez.")

        await interaction.response.send_message(embed=embed, view=pollview)
        
class PollView(discord.ui.View):
    def __init__(self, opcoes: list[str]):
        super().__init__()
        self.opcoes = opcoes
        self.votos = {opcao: 0 for opcao in opcoes}
        self.already_vote = set()
        for indice, opcao in enumerate(opcoes):
            button = discord.ui.Button(
                label=opcao,
                style=discord.ButtonStyle.primary,
                custom_id=str(indice)
            )

            button.callback = self.clicked

            self.add_item(button)
    
    async def clicked(self, interaction: discord.Interaction):
        if interaction.user.id in self.already_vote:
            await interaction.response.send_message("Voce já votou", ephemeral=True)
            return
        
        if interaction.data is None:
            return
        
        custom_id = interaction.data.get("custom_id")

        if custom_id is None:
            return
        
        voted_option = self.opcoes[int(custom_id)]
            
        self.votos[voted_option] += 1

        if interaction.message is None:
            return

        embed = interaction.message.embeds[0]

        for index, option in enumerate(embed.fields):
            if option.name == voted_option:
                embed.set_field_at(
                    index=index,
                    name=option.name,
                    value=f"{self.votos[voted_option]} votos"
                    )
        await interaction.response.edit_message(embed=embed)

        self.already_vote.add(interaction.user.id)
        await interaction.followup.send("Voto registrado", ephemeral=True)
    
async def setup(bot: commands.Bot):
    await bot.add_cog(Poll(bot))