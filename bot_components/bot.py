# path: bot.py
import discord
from discord.ext import tasks
from jobspy import scrape_jobs
from .config import load_config
import subprocess
import csv
import json
import os

class Nanéu(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config = load_config()

    async def on_ready(self):
        print(f'We have logged in as {self.user}')
        self.scrape_and_post.start()

    @tasks.loop(hours=12)
    async def scrape_and_post(self):
        jobs = scrape_jobs(
            site_name= self.config['site_name'],
            search_term=self.config['search_term'],
            location=self.config['location'],
            results_wanted=self.config['results_wanted'],
            hours_old=self.config['hours_old'],
            country_indeed=self.config['country_indeed'],
        )

        jobs.to_csv("jobs.csv", quoting=csv.QUOTE_NONNUMERIC, escapechar="\\", index=False)
        subprocess.run(["python", "bot_components/jsonify.py"])

        with open('jobs.json', 'r') as f:
            jobs_json = json.load(f)
        
        embeds = []
        channel = self.get_channel(self.config['channel_id'])
        if not os.path.exists('posted_jobs.txt'):
            open('posted_jobs.txt', 'w').close()
        try:
            with open('posted_jobs.txt', 'r') as f:
                posted_jobs = [line.strip() for line in f]
        except Exception as e:
            print(f"Failed to read from posted_jobs.txt: {str(e)}")
            return
        for job in jobs_json:
            job_id = f"{job['job_url']},{self.config['channel_id']}"
            if job_id in posted_jobs:
                continue
            else:
                with open('posted_jobs.txt', 'a') as f:
                    f.write(f"{job_id}\n")
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
                print(f"Sent message to Discord: {embed.title}")
        except Exception as e:
            print(f"Failed to send message to Discord: {str(e)}")
            return