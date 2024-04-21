# path: bot_components/bot.py
import discord
from discord.ext import commands, tasks
from jobspy import scrape_jobs
from bot_components.config import load_config
from twitter_bot.twitter_manager import TwitterManager
import subprocess
import csv
import json
import os
import asyncio

class Nanéu(commands.Bot):
    """
    A custom bot class for Nanéu.

    This class extends the `commands.Bot` class and provides additional functionality for the Nanéu bot.

    Attributes:
        config (dict): The configuration settings for the bot.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config = None
        self.job_queue = asyncio.Queue()
        self.queues = {}
        self.send_jobs.start()

    async def on_ready(self):
        """
        Event handler for when the bot is ready.

        This method is called when the bot has successfully logged in and is ready to start processing events.
        It prints the bot's user information and the number of guilds it is a member of, and starts the `scrape_and_post` task.
        """
        print(f'scrapper is logged in as {self.user}')
        print(f'Bot is a member of {len(self.guilds)} guilds') 
        self.scrape_and_post.start()
    
    async def close(self):
        """
        Closes the bot.

        This method cancels the `scrape_and_post` task and then calls the `close` method of the base class.
        """
        self.scrape_and_post.cancel()
        await super().close()

    async def on_guild_join(self, guild):
        """
        Event handler for when the bot joins a guild.

        This method is called when the bot joins a new guild.
        It sends a welcome message to the system channel of the guild (if the bot has permission to send messages),
        and sends a notification message to the bot admin user.
        
        Args:
            guild (discord.Guild): The guild that the bot joined.
        """
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
    async def send_jobs(self):
        for channel_id, queue in list(self.queues.items()):
            if queue:
                job = queue.popleft()
                channel = self.get_channel(channel_id)
                try:
                    await channel.send(embed=job)
                except Exception as e:
                    print(f"Failed to send message to Discord: {str(e)}")
            else:
                del self.queues[channel_id]

    async def scrape_and_post(self):
        """
        Task that periodically scrapes job listings and posts them to Discord.

        This task is scheduled to run every 60 seconds.
        It iterates over all the guilds that the bot is a member of, and for each guild,
        it iterates over the text channels and checks if there is a configuration for the channel.
        If a configuration is found, it scrapes job listings and posts them to the channel.
        """
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

# TODO: this function post to twitter and discord for now
    async def scrape_and_post_to_discord(self, channel):
        twitter_manager = TwitterManager()  # Initialize the TwitterManager
        """
        Scrapes job listings and posts them to a Discord channel.

        This method scrapes job listings based on the configuration settings for the given channel,
        and then creates embeds for each job listing and sends them to the channel.

        Args:
            channel (discord.TextChannel): The channel to post the job listings to.
        """
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
            if channel.id not in self.queues:
                self.queues[channel.id] = asyncio.Queue()
            self.queues[channel.id].put(job)
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

                # check if it is possible to post to x today
                try:
                    if twitter_manager.can_post_today():
                        twitter_manager.post_job(job)
                    else:
                        print("Twitter posting limit reached for today.")
                except Exception as e:
                    print(f"Error posting to Twitter: {e}")
        
        try:
            for embed in embeds:
                await channel.send(embed=embed)
                print(f"Sent message to Discord: {embed.title}")
        except Exception as e:
            print(f"Failed to send message to Discord: {str(e)}")
