from typing import ValuesView
import discord 
from discord.ext import commands 


class Administrator(commands.Cog):

    def __init__(self, bot): 
        self.bot = bot

    # bans a user 
    @commands.command()
    async def ban(self, ctx, member:discord.Member = None, reason = "None Given."):
        try:
            if member == ctx.message.author:
                await ctx("Can not ban yourself.")
                return 
            if member is None:
                await ctx.send("Member must be specified.")
                return
            else:
                em = discord.Embed(title=f"Banned {member}!", description=f"Reason: {reason} By: {ctx.author.mention}")
                await member.send(f'You have been banned form {ctx.guild.name} for {reason}')
                await ctx.channel.send(embed=em)
                await member.ban(reason=reason)

        except:
            await ctx.send(f'Error in banning {member} from the server.')

    # unbans a user 
    @commands.command()
    async def unban(self, ctx, *, member):
        try:
            x = int(member)
            banned_users = await ctx.guild.bans()

            for ban_entry in banned_users:
                user = banned_users.user
                if user.id == x:
                    await ctx.guild.unban(user)
                    await ctx.send(f'Unbanned {user.mention}')
                    return 

        except ValueError:
            banned_users = await ctx.guild.bans()
            member_name, member_discriminator = member.split("#")
            for ban_entry in banned_users:
                user = ban_entry.user
                if((user.name, user.discriminator) == (member_name, member_discriminator)):
                    await ctx.guild.unban(user)
                    await ctx.send(f'Unbanned {user.mention}')                    
                    return 

    

def setup(bot):
    bot.add_cog(Administrator(bot))