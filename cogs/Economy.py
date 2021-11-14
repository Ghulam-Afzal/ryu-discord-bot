import discord
from discord.ext import commands 



class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot 
        self.jobs = {'peasant': [1, 0], 'yard worker': [5, 3000], "farmer": [9, 6000], "secretary": [11, 9000], "military": [15, 12000], "dentist": [25, 15000]}


    @commands.command()
    async def list_jobs(self, ctx):
        em = discord.Embed(title=f"The Availble jobs currently are the following: ")

        for job in self.jobs:
            em.add_field(name=f"{job}", value=f"the income of this job is {self.jobs[job][0]} and it costs {self.jobs[job][1]}", inline=False)

        await ctx.send(embed=em)
        return 


    @commands.command()
    async def signup(self, ctx):
        # db = await aiosqlite.connect("ryu.db")
        cursor = await self.bot.db.execute(f"SELECT job FROM economyTable WHERE guild_id = {ctx.guild.id} AND user_id = {ctx.author.id}")
        result = await cursor.fetchone()
            
        if result is None:
            sql = ("INSERT INTO economyTable (guild_id, user_id, job, wallet, bank) VALUES(?, ?, ?, ?, ?)")
            val = (ctx.guild.id, ctx.author.id, "None", 0, 0)
            await self.bot.db.execute(sql, val)
            await ctx.send("Account has been created.")
        
        else: 
            await ctx.send("You already have a account.")
        
        await self.bot.db.commit()
        await cursor.close()
        return 


    # a make a people be able to perform jobs 
    # command to select a job
    @commands.command()
    async def select_job(self, ctx, *, job=None):

        if job is None:
            await ctx.send("Please specify a job, if you do not know any use list_jobs to see the full list of jobs available.")    
        else:
            # update the users data in the table, to change the new job
            cursor = await self.bot.db.execute(f"SELECT job FROM economyTable WHERE guild_id = {ctx.guild.id} AND user_id = {ctx.author.id}")
            result = await cursor.fetchone()
            
            if result is None:
                await ctx.send("You do not have a account. Use !signup to make a account.")
            else:
                sql = ("UPDATE economyTable SET job = ? WHERE guild_id = ? AND user_id = ?")
                val = (job, ctx.guild.id, ctx.author.id)
                await self.bot.db.execute(sql, val)
                em = discord.Embed(title=f"You have chosen to work as a {job}")
                await ctx.send(embed=em)
                
            await self.bot.db.commit()
            await cursor.close()

            return 





    # allow the user to get a daily
    @commands.command()
    @commands.cooldown(1, 86400, commands.BucketType.user)
    async def daily(self, ctx):
        em = discord.Embed(title=f"You have claimed your daily of 1000 ")

        # update the daily counter by giving the person a 1000
        cursor = await self.bot.db.execute(f"SELECT wallet FROM economyTable WHERE guild_id = {ctx.guild.id} AND user_id = {ctx.author.id}")
        result = await cursor.fetchone()

        if result is None:
            await ctx.send("You do not have a account. Use !signup to make a account. Now you wait a day before you can claim.")
        elif result is not None:
            sql = ("UPDATE economyTable SET wallet = wallet + 1000 WHERE guild_id = ? AND user_id = ?")
            val = (ctx.guild.id, ctx.author.id)
            await self.bot.db.execute(sql, val)
            await ctx.channel.send(embed=em)

        await self.bot.db.commit()
        await cursor.close()



        return 


    @commands.command()
    @commands.cooldown(1, 28800, commands.BucketType.user)
    async def work(self, ctx):
        
        cursor = await self.bot.db.execute(f"SELECT job FROM economyTable WHERE guild_id = {ctx.guild.id} AND user_id = {ctx.author.id}")
        result = await cursor.fetchone()

        if result is None:
            embed = discord.Embed(titile="You do not have a job selected.")
            await ctx.send(embed=embed)

        else:
            wage = self.jobs[result[0]][0] * 8 
            sql = ("UPDATE economyTable SET wallet = wallet + ? WHERE guild_id = ? AND user_id = ?")
            val = (wage, ctx.guild.id, ctx.author.id)
            await self.bot.db.execute(sql, val)
            embed = discord.Embed(title=f"you have earned {wage} today.")
            await ctx.send(embed=embed)
        await self.bot.db.commit()
        await cursor.close()
        return 

    # command to depsoti money from your wallet into you bank account
    @commands.command()
    async def dep(self, ctx, *, amount="test"):

        cursor = await self.bot.db.execute(f"SELECT wallet FROM economyTable WHERE guild_id = {ctx.guild.id} AND user_id = {ctx.author.id}")
        result = await cursor.fetchone()

        if result is None:
                embed =  discord.Embed(title=f"You dont have any money to depsit. Go work.")
                await ctx.send(embed=embed)
                return 

        try:
            amt = int(amount)
            if result[0] < amt:
                embed = discord.Embed(title="You do not have that much money.")
                await ctx.send(embed=embed)
                return 
                
            else:
                embed =  discord.Embed(title=f"You have deposited {amt} into your account")
                val = (amt, ctx.guild.id, ctx.author.id)
                await self.bot.db.execute("UPDATE economyTable SET bank = bank + ? WHERE guild_id = ? AND user_id = ?", val)
                await self.bot.db.execute("UPDATE economyTable SET wallet = wallet - ? WHERE guild_id = ? AND user_id = ?", val)
                await ctx.send(embed=embed)

                await self.bot.db.commit()
                await cursor.close()
                return 

        except ValueError:
            embed =  discord.Embed(title=f"Enter a valid amount of money to deposit.")
            await ctx.send(embed=embed)
            return 

    # command to with draw money from your bank into your wallet for use
    @commands.command()
    async def withdraw(self, ctx, *, amount="test"):
        
        cursor = await self.bot.db.execute(f"SELECT bank FROM economyTable WHERE guild_id = {ctx.guild.id} AND user_id = {ctx.author.id}")
        result = await cursor.fetchone()

        if result is None:
                embed = discord.Embed(title=f"You dont have any money to withdraw.")
                await ctx.send(embed=embed)
                return 

        try:
            amt = int(amount)
            if result[0] < amt:
                embed = discord.Embed(title="You do not have that much money.")
                await ctx.send(embed=embed)
                return 
                
            else:
                embed =  discord.Embed(title=f"You have withdrawm {amt} into your account")
                val = (amt, ctx.guild.id, ctx.author.id)
                await self.bot.db.execute("UPDATE economyTable SET wallet = wallet + ? WHERE guild_id = ? AND user_id = ?", val)
                await self.bot.db.execute("UPDATE economyTable SET bank = bank - ? WHERE guild_id = ? AND user_id = ?", val)
                await ctx.send(embed=embed)

                await self.bot.db.commit()
                await cursor.close()
                return 

        except ValueError:
            embed = discord.Embed(title=f"Enter a valid amount of money to deposit.")
            await ctx.send(embed=embed)
            return 

    @commands.command()
    async def bal(self, ctx, *, user=None):
        embed  = discord.Embed(title="Your balance is:")

        if user is None: 
            val = (ctx.guild.id, ctx.author.id)
            cursor = await self.bot.db.execute("SELECT wallet, bank FROM economyTable WHERE guild_id = ? AND user_id = ?", val)
            result = await cursor.fetchone()
            if result is None: 
                embed.add_field(name="Wallet", value="0", inline=True)
                embed.add_field(name="Bank", value="0", inline=True)

            else:
                embed.add_field(name="Wallet", value=result[0], inline=True)
                embed.add_field(name="Bank", value=result[1], inline=True)

            await ctx.send(embed=embed)
            return 
        else: 
            await ctx.send("You can only check your own balance")

        return


def setup(bot):
    bot.add_cog(Economy(bot))