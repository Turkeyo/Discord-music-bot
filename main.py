import asyncio
from discord.ext import commands
import discord
import os
from dotenv import load_dotenv, dotenv_values
from discord.flags import Intents

Intents = discord.Intents.all()
Intents.message_content = True

# Set prefix
bot = commands.Bot(command_prefix="!", intents=Intents)
# Remove initialization command 'help'
bot.remove_command("help")

# Online bot
@bot.event
async def on_ready():
        print(f"{bot.user} is ready")

# Load commands
async def main():
    async with bot:
        for Filename in os.listdir("./cmds"):
            if Filename.endswith(".py"):
                await bot.load_extension(f"cmds.{Filename[:-3]}")
                print(f"Load {Filename[:-3]} success...")
        load_dotenv()
        TOKEN = os.getenv("discord_token")
        await bot.start(TOKEN)

if __name__ == "__main__":
    asyncio.run(main())
