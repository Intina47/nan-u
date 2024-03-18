# path: cog/setup.py
from discord.ext import commands
import yaml

class Setup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def setup(self, ctx):
        def check(message):
            print(f"message.author: {message.author}, ctx.author: {ctx.author}, message.channel: {message.channel}, ctx.channel: {ctx.channel}")
            return message.author == ctx.author and message.channel == ctx.channel

        await ctx.send("Please enter the job titles you're interested in (comma-separated). For example: software engineer, devops engineer.")
        search_terms = await self.bot.wait_for('message', check=check)
        search_terms = search_terms.content

        await ctx.send("Please enter the location where you're looking for jobs. For example: Edinburgh, Scotland, United Kingdom.")
        location = await self.bot.wait_for('message', check=check)
        location = location.content

        await ctx.send("Please enter the maximum age of the job postings you're interested in (in hours). For example, enter '72' for job postings that are up to 3 days old.")
        hours_old = await self.bot.wait_for('message', check=check)
        hours_old = int(hours_old.content)

        await ctx.send("Please enter the country where you're looking for jobs. For example: uk.")
        country_indeed = await self.bot.wait_for('message', check=check)
        country_indeed = country_indeed.content

        config = {}
        config['channel_id'] = ctx.channel.id
        config['site_names'] = ['linkedin']  # Default site name
        config['search_terms'] = search_terms
        config['location'] = location
        config['results_wanted'] = 10  # Default number of results
        config['hours_old'] = hours_old
        config['country_indeed'] = country_indeed  # Default country

        file_path = f'./config/config_{ctx.channel.id}.yaml'
        with open(file_path, 'w') as f:
            yaml.dump(config, f)

        await ctx.send("Setup complete!")

async def setup(bot):
    await bot.add_cog(Setup(bot))



