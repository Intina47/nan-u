# path: app.py
import os
import asyncio
import discord
from discord.ext import commands
from dotenv import load_dotenv
from bot_components.bot import Nanéu
from utils.errors import DiscordTokenErrors

# Load the .env file
load_dotenv()

def get_prefix(bot, message):
    prefix = f'<@!{bot.user.id}> !'
    return commands.when_mentioned_or(prefix)(bot, message)

async def load():
    cog_dir = './cog'
    for filename in os.listdir(cog_dir):
        file_path = os.path.join(cog_dir, filename)
        if os.path.isfile(file_path) and filename.endswith('.py'):
            await bot.load_extension(f'cog.{filename[:-3]}')
            if bot.load_extension:
                print(f'Loaded {filename[:-3]} cog')
            else:
                print(f'Failed to load {filename[:-3]} cog')


intents = discord.Intents.default()
intents.messages = True 
intents.message_content = True
bot = Nanéu(command_prefix=get_prefix,intents=intents)

async def main():
    await load()
    discord_token = os.getenv('DISCORD_TOKEN')
    if discord_token is None:
        DiscordTokenErrors.token_not_set_error()
        return
    else:
        try:
            await bot.start(discord_token)
        except discord.LoginFailure:
            DiscordTokenErrors.invalid_token_error()
            return

asyncio.run(main())
