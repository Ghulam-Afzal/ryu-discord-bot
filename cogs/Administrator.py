import discord 
from discord.ext import commands 
from discord.ext.commands.errors import MemberNotFound
import asyncio 


class Administrator(commands.Cog):

    def __init__(self, bot): 
        self.bot = bot

    # bans a user 
    @commands.command()
    @commands.has_permissions(administrator=True)
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
    @commands.has_permissions(administrator=True)
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

    @commands.command() 
    @commands.has_permissions(administrator=True)
    async def setlvl(self, ctx, member: discord.Member = None, *,  level=None):

        # if the lvl was not specified then ask for it to be specified 
        if level is None:
            return await ctx.send('There was no reset level specified.')
        
        # if the level parameter is not a number then ask for it to be entered as a number 
        try: 
            check_if_level_is_int = int(level)
            
            # if member was specified, then continue with the command 
            if member is not None: 
                try: 
                    await ctx.send(f'Are you sure you want the level for {member.mention} to be set to {level}. Response must be yes/no.')
                    response = await self.bot.wait_for('message', timeout=60.0)
                
                    # if the response is a yes then reset the level of the user
                    if response.content.lower() == 'yes': 
                        await self.bot.db.execute('UPDATE levelData SET lvl = ? WHERE guild_id = ? AND user_id = ?', (level, ctx.guild.id, member.id))
                        await self.bot.db.execute('UPDATE levelData SET exp = ? WHERE guild_id = ? AND user_id = ?', (0, ctx.guild.id, member.id))
                        await ctx.send(f'The level for {member} has been set to {level}')

                    # else cancel the command 
                    else: 
                        return await ctx.send('Command was canceled.')

                except asyncio.TimeoutError: 
                    return await ctx.send('Command timed out.')
        
        
        except ValueError: 
            return await ctx.send('Level must be a number')
        
        except MemberNotFound: 
            return await ctx.send('Membe was not found')

def setup(bot):
    bot.add_cog(Administrator(bot))