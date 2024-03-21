# path: app.py
import asyncio
import os
import discord
from discord.ext import commands
from bot_components.bot import Nanéu

def get_prefix(bot, message):
    prefix = f'<@!{bot.user.id}> !'
    return commands.when_mentioned_or(prefix)(bot, message)

async def load():
    for filename in os.listdir('./cog'):
        if filename.endswith('.py'):
            await bot.load_extension(f'cog.{filename[:-3]}')
            print(f"Loaded {filename}.")
        else:
            print(f"Failed to load {filename}: not a .py file.")

intents = discord.Intents.default()
# intents.messages = True 
# intents.message_content = True
bot = Nanéu(command_prefix=get_prefix,intents=intents)

async def main():
    await load()
    discord_token = os.getenv('DISCORD_TOKEN')
    await bot.start(discord_token)

asyncio.run(main())
