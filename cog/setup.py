import asyncio
from discord.ext import commands
import yaml
import os

class Setup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.setup_processes = {}

    @commands.command(name='setup', help="Configure Nanéu to your preferences. make sure you have the right permissions. which is administrator, manage_guild, manage_channels")
    @commands.has_permissions(administrator=True, manage_guild=True, manage_channels=True)
    async def setup(self, ctx):
        if ctx.author in self.setup_processes:
            self.setup_processes[ctx.author].cancel()
            del self.setup_processes[ctx.author]  # Delete the old setup process

        try:
            self.setup_processes[ctx.author] = self.bot.loop.create_task(self.setup_process(ctx))
            await self.setup_processes[ctx.author]
        except asyncio.CancelledError:
            await ctx.send("Setup cancelled.")
        finally:
            if ctx.author in self.setup_processes:
                del self.setup_processes[ctx.author]
            await ctx.send("Setup complete!")

    async def setup_process(self, ctx):
        try:
            config = await asyncio.wait_for(self.get_config(ctx), timeout=60)
            if config is not None:
                await self.save_config(ctx.channel.id, config)
            else:
                await ctx.send("Setup cancelled due to inactivity.")
        except asyncio.TimeoutError:
            await ctx.send("Setup cancelled due to inactivity.")
            config = None
        return config
 
    
    async def get_config(self, ctx):
        try:
            def check(message):
                return message.author.id == ctx.author.id and message.channel == ctx.channel

            search_terms = await self.ask_question(ctx, "Please enter the job titles you're interested in (comma-separated). For example: software engineer, devops engineer.", check)
            location = await self.ask_question(ctx, "Please enter the location where you're looking for jobs. For example: Edinburgh, Scotland, United Kingdom.", check)
            hours_old = await self.ask_question(ctx, "Please enter the maximum age of the job postings you're interested in (in hours). For example, enter '72' for job postings that are up to 3 days old.", check)
            country_indeed = await self.ask_question(ctx, "Please enter the country where you're looking for jobs. For example: uk.", check)

            config = {
                'channel_id': ctx.channel.id,
                'site_names': ['linkedin'],  # Default site name
                'search_terms': search_terms,
                'location': location,
                'results_wanted': 10,  # Default number of results
                'hours_old': hours_old,
                'country_indeed': country_indeed
            }

            return config
        except Exception as e:
            await ctx.send(f"An error occurred while getting the configuration: {e}")
            return None
    
    async def ask_question(self, ctx, question, check, conversion=str):
        while True:  # Keep asking the question until a non-empty answer is received
            await ctx.send(question)
            try:
                answer = await self.bot.wait_for('message', check=check, timeout=60)  # Wait for 60 seconds
            except asyncio.TimeoutError:
                print(f"No answer received for question: {question}")
                return None
            if answer.content.strip():  # Check if the answer is not an empty string
                print(f"Received answer: {answer.content}")
                return answer.content if conversion is str else await conversion(answer.content)
            else:
                await ctx.send("Your answer cannot be empty. Please try again.")

    async def save_config(self, channel_id, config):
        try:
            configdir = './config'
            if not os.path.exists(configdir):
                os.makedirs(configdir)
            file_path = f'./config/config_{channel_id}.yaml'
            with open(file_path, 'w') as f:
                yaml.dump(config, f)
        except Exception as e:
            print(f"An error occurred while saving the configuration: {e}")

    @setup.error
    async def setup_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(f"Sorry {ctx.author} you don't have the right permissions to run {ctx.command} command")
        else:
            await ctx.send("An error occurred while setting up the bot. Please try again.")
            print("An error occurred while setting up the bot. Please try again.", error)

async def setup(bot):
    await bot.add_cog(Setup(bot))
