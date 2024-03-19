# path: cog/setup.py
import asyncio
from discord.ext import commands
import yaml

class Setup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.setup_processes = {}

    @commands.command(name='setup', help="Configure the Nanéu to your preferences.")
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
        config = await self.get_config(ctx)
        self.save_config(ctx.channel.id, config)
        return config    
    
    async def get_config(self, ctx):
        try:
            def check(message):
                return message.author == ctx.author and message.channel == ctx.channel

            search_terms = await self.ask_question(ctx, "Please enter the job titles you're interested in (comma-separated). For example: software engineer, devops engineer.", check)
            location = await self.ask_question(ctx, "Please enter the location where you're looking for jobs. For example: Edinburgh, Scotland, United Kingdom.", check)
            while True:
                hours_old = await self.ask_question(ctx, "Please enter the maximum age of the job postings you're interested in (in hours). For example, enter '72' for job postings that are up to 3 days old.", check)
                try:
                    hours_old = int(hours_old)
                    break
                except ValueError:
                    await ctx.send("Invalid input. Please enter a number. Example: 72. for 3 days old job postings.")
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
        await ctx.send(question)
        answer = await self.bot.wait_for('message', check=check)
        return conversion(answer.content)

    def save_config(self, channel_id, config):
        try:
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
