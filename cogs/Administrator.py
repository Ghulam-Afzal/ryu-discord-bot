import discord 
from discord.ext import commands 
from discord.ext.commands.errors import MemberNotFound
import asyncio 


class Administrator(commands.Cog):

    def __init__(self, bot): 
        self.bot = bot

    # bans a user 
    @commands.command(name='ban', help='Bans a member.')
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
    @commands.command(name='unban', help='Unbans a member.')
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

    @commands.command(name='kick', help='Kicks a member.')
    @commands.has_permissions(kick_members=True)
    async def kick_member(self, ctx, member: discord.Member = None, *, reason="No reason given"):
        try:
            if member == ctx.message.author:
                await ctx.send('Can not kick yourself.')
                return
            
            if member is None:
                await ctx.send('A member must be specified.')
                return
            
            else:
                message = f'You have been kicked form {ctx.guild.name} for {reason}'
                em = discord.Embed(title=f"Kicked {member}!",
                                description=f"Reason: {reason} By: {ctx.author.mention}")
                await member.send(message)
                await ctx.channel.send(embed=em)
                await member.kick(reason=reason)
                
        except:
            await ctx.send(f'Error in kicking {member} from the server.')


    @commands.command(aliases=['crch', 'create-channel', 'create-ch'],
             help='Allows you to create text channels\n takes channel name as the input.')
    @commands.has_permissions(administrator=True)
    async def create_text_channel(self, ctx, channel_name):
        
        # get the existing channels
        existing_channel = discord.utils.get(ctx.guild.channels, name=channel_name)
        
        # check if the name of the channel is passed as a arg
        if channel_name is None:
            await ctx.send('A channel name is required.')
            
        # if the channel does not exist already then create one
        if not existing_channel:
            await ctx.send(f'New channel created named:  {channel_name}')
            await ctx.guild.create_text_channel(channel_name)
            
        # if it already exists tell the member that it does
        else:
            await ctx.send(f'{channel_name} already exits.')


    @commands.command(aliases=['dlch', 'delete-channel', 'delete-ch'],
                help='Allows you to delete text channels\n takes channel name as the input.')
    @commands.has_permissions(administrator=True)
    async def delete_channel(self, ctx, channel_name):
        
        # check is the channel that is entered exists
        existing_channel = discord.utils.get(ctx.guild.channels, name=channel_name)
        if channel_name is None:
            await ctx.send('A channel name is required.')
            
        # if it exists delete it
        if existing_channel is not None:
            await existing_channel.delete()
            await ctx.send(f'{channel_name} was deleted.')
            
        # if it does not exist inform the user
        else:
            await ctx.send(f'{channel_name} could not be found.')


    @commands.command(name='setlvl', help='Sets a users level.') 
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
                        await ctx.send(f'The level for {member.mention} has been set to {level}')

                    # else cancel the command 
                    else: 
                        return await ctx.send('Command was canceled.')

                except asyncio.TimeoutError: 
                    return await ctx.send('Command timed out.')
        
        
        except ValueError: 
            return await ctx.send('Level must be a number')
        
        except MemberNotFound: 
            return await ctx.send('Member was not found')

def setup(bot):
    bot.add_cog(Administrator(bot))