import os 
import discord 
from discord.ext import commands 
import aiosqlite

class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot 
        self.bot.db = aiosqlite.connect("economyDB.db")
        self.jobs = {'peasant': 1, 'yard worker': 5}

    # a make a people be able to perform jobs 
    # command to select a job
    @commands.command()
    async def select_job(self, ctx, job):
        if job is None:
            em = discord.Embed(title=f"The Availble jobs currently are the following: ")

            for job, base_income in self.jobs:
                em.add_field(name=f"{job}", value=f"the income of this job is {base_income}")
            await ctx.send(em)
        else:
            await self.bot.db.execute("CREATE TABLE IF NOT EXISTS economyTable (guild_id int, user_id int, job text, bank int, PRIMARY KEY (guild_id, user_id))")
            # update the users data in the table, to change the new job
            await ctx.send(f"You have chosen to work as a {job}")
            return 





    # allow the user to get a daily
    @commands.command()
    async def daily(self, ctx):
        embed = discord.Embed(title=f"Yo have claimed your daily of 1000 ")
        
        # update the daily counter by giving the person a 1000
        await self.bot.db.execute('UPDATE economyTable SET bank = bank + 1000 WHERE guild_id = ? AND user_id = ?', )
        await ctx.send(embed)
        return 

def setup(bot):
    bot.add_cog(Economy(bot))