# path: app.py
import os
from bot_components.bot import Nanéu
import discord

discord_token = os.getenv('DISCORD_TOKEN')
intents = discord.Intents.default()
bot = Nanéu(intents=intents)
bot.run(discord_token)