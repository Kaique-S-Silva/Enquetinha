import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

from src.database.connection import create_tables

load_dotenv()

TOKEN: str | None = os.getenv("TOKEN")

class MyBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        super().__init__(command_prefix=".", intents=intents)
    
    async def setup_hook(self):
        await create_tables()
        for filename in os.listdir("./src/commands"):
            if filename.endswith(".py"):
                await self.load_extension(f"src.commands.{filename[:-3]}")
                print(f"Extension loaded: {filename}")
        await self.tree.sync()
    
    async def on_ready(self):
        print(f"Logged as {self.user}")
    
    async def on_guild_join(self, guild):
        if str(guild.id) != os.getenv("ALLOWED_GUILD_ID"):
            print("Servidor não autorizado")
            await guild.leave()

bot = MyBot()

if TOKEN:
    bot.run(TOKEN)