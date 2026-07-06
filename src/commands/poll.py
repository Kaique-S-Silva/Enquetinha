import discord
from discord import app_commands
from discord.ext import commands

from src.database.connection import create_poll
from src.utils.formatting import emoji_slash
import src.views.poll_view_select as pv

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
        
        poll_id, options_id = await create_poll(pergunta, optionsNotNone, interaction.user.id, interaction.guild_id)

        pollview = pv.PollView(optionsNotNone, poll_id, options_id, tempo)

        embed = discord.Embed(
            title=pergunta,
            description="Vote usando os botões abaixo!",
            color=discord.Color.blurple()
        )

        for field in optionsNotNone:
            embed.add_field(name=field, value=f"{emoji_slash(0, 0)} {0} votos", inline=False)

        embed.set_footer(text="Cada pessoa pode votar apenas uma vez.")

        await interaction.response.send_message(embed=embed, view=pollview)

        pollview.message = await interaction.original_response()


    
async def setup(bot: commands.Bot):
    await bot.add_cog(Poll(bot))