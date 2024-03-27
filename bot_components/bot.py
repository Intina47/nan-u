# path: bot_components/bot.py
import discord
from discord.ext import commands, tasks
from jobspy import scrape_jobs
from bot_components.config import load_config
import subprocess
import csv
import json
import os
import asyncio

class Nanéu(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config = None

    async def on_ready(self):
        print(f'scrapper is logged in as {self.user}')
        print(f'Bot is a member of {len(self.guilds)} guilds') 
        self.scrape_and_post.start()
    
    async def close(self):
        self.scrape_and_post.cancel()
        await super().close()

    async def on_guild_join(self, guild):
        system_channel = guild.system_channel
        if system_channel is not None and system_channel.permissions_for(guild.me).send_messages:
            await system_channel.send("Thanks for invite!\nPlease run/type `@nanéu setup` command on the channel you wish me to post, to configure me to your liking.")
        try:
            my_user_id = os.getenv('NANEU_ADMIN_USER_ID')
            user = await self.fetch_user(my_user_id)
            await user.send(f"{guild.name} added Nanéu to their server. the channel id is {guild.id}")
        except Exception as e:
            print(f"Failed to send message to admin: {str(e)}")

    @tasks.loop(seconds=60)
    async def scrape_and_post(self):
        print('Entered scrape_and_post loop')
        for guild in self.guilds:
            print(f'Checking guild {guild.id}')
            for channel in guild.text_channels:
                print(f'Checking channel {channel.id}')
                loop = asyncio.get_event_loop()
                self.config = await loop.run_in_executor(None, load_config, channel.id)
                print(f"Configuration for channel {channel.id}: {self.config}")  # Add this line
                if self.config is not None:
                    await self.scrape_and_post_to_discord(channel)
                    print(f"Scraped and posted to Discord for channel {channel.id}")
                else:
                    print("Configuration not found. Please run the !setup command.")

    async def scrape_and_post_to_discord(self, channel):
        print(f"2.Entered scrape_and_post_to_discord for channel {channel.id}")
        # make scraping run on a separate thread in the background to avoid blocking the event loop
        loop = asyncio.get_event_loop()
        scrape_jobs_args = {
            'site_name': self.config['site_names'],
            'search_term': self.config['search_terms'],
            'location': self.config['location'],
            'results_wanted': self.config['results_wanted'],
            'hours_old': self.config['hours_old'],
            'country_indeed': self.config['country_indeed']
        }
        try:
            jobs = await loop.run_in_executor(None, lambda: scrape_jobs(**scrape_jobs_args))
        except Exception as e:
            print(f"Failed to scrape jobs: {str(e)}")
            return

        print(f"Scraped jobs for channel {channel.id}")
        jobs.to_csv("jobs.csv", quoting=csv.QUOTE_NONNUMERIC, escapechar="\\", index=False)
        subprocess.run(["python", "bot_components/jsonify.py"])
        print(f"Finished scrape_and_post_to_discord for channel {channel.id}")

        with open('jobs.json', 'r') as f:
            jobs_json = json.load(f)
        
        embeds = []
        posted_jobs_file_path = '/app/config/posted_jobs.txt'
        if not os.path.exists(posted_jobs_file_path):
            open(posted_jobs_file_path, 'w').close()
        try:
            with open( posted_jobs_file_path, 'r') as f:
                posted_jobs = [line.strip() for line in f]
        except Exception as e:
            print(f"Failed to read from posted_jobs.txt: {str(e)}")
            return
        for job in jobs_json:
            job_id = f"{job['job_url']},{self.config['channel_id']}"
            if job_id in posted_jobs:
                continue
            else:
                with open(posted_jobs_file_path, 'a') as f:
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
