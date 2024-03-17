from flask import Flask, jsonify
import discord
from discord.ext import tasks
import requests
import pandas as pd 
from jobspy import scrape_jobs
import subprocess
import csv
import yaml
import json
import os

app = Flask(__name__)
discord_token = os.getenv('DISCORD_TOKEN')

with open('./config/config.yaml', 'r') as f:
            config = yaml.safe_load(f)

class Nanéu(discord.Client):
    async def on_ready(self):
        print(f'We have logged in as {self.user}')
        self.scrape_and_post.start()

    # async def on_message(self, message):
    #     print(f'{message.channel}: {message.author}: {message.author.name}: {message.content}')

    @tasks.loop(seconds=30)
    async def scrape_and_post(self):
        jobs = scrape_jobs(
            site_name= config['site_name'],
            search_term=config['search_term'],
            location=config['location'],
            results_wanted=config['results_wanted'],
            hours_old=config['hours_old'],
            country_indeed=config['country_indeed'],
        )

        jobs.to_csv("jobs.csv", quoting=csv.QUOTE_NONNUMERIC, escapechar="\\", index=False)
        subprocess.run(["python", "jsonify.py"])

        with open('jobs.json', 'r') as f:
            jobs_json = json.load(f)
        
        embeds = []
        channel = self.get_channel(config['channel_id'])
        for job in jobs_json:
            embed = discord.Embed(
                title=job['title'],
                url=job['job_url'],
                color=discord.Color.blue()
            )
            embed.add_field(name="Company", value=job['company'], inline=True)
            embed.add_field(name="Location", value=job['location'], inline=True)
            embeds.append(embed)
        try:
            for embed in embeds:
                await channel.send(embed=embed)
        except Exception as e:
            print(f"Failed to send message to Discord: {str(e)}")
            return
        
intents = discord.Intents.default()
bot = Nanéu(intents=intents)
bot.run(discord_token)
