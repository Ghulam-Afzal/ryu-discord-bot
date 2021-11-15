import random
from discord.ext import commands
import discord

class Level(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_message(self, message):
  
        if not message.author.bot: 
            cursor = await self.bot.db.execute('''
            INSERT OR IGNORE INTO levelData 
            (guild_id, user_id, lvl, exp, msg_count)
            VALUES(?,?,?,?,?)
            ''', (message.guild.id, message.author.id, 1, 0, 0))

            if cursor.rowcount == 0: 
                exp_given = random.randint(15, 25)
                await self.bot.db.execute('''
                UPDATE levelData 
                SET exp = exp + ? 
                WHERE guild_id = ? AND user_id = ?
                ''', (exp_given, message.guild.id, message.author.id))

                await self.bot.db.execute('''
                UPDATE levelData 
                SET msg_count = msg_count + 1 
                WHERE guild_id = ? AND user_id = ?
                ''', (message.guild.id, message.author.id))

                cur = await self.bot.db.execute('''
                SELECT exp FROM levelData
                WHERE guild_id = ? AND user_id = ?
                ''', (message.guild.id, message.author.id))

                curr_lvl = await self.bot.db.execute('''
                SELECT lvl FROM levelData 
                WHERE guild_id = ? AND user_id = ?
                ''', (message.guild.id, message.author.id))
                data = await cur.fetchone() 
                exp = data[0]
                temp = await curr_lvl.fetchone()
                lvl = temp[0]
                print(lvl)

                # calc exp required for next level and then update the level in db
                exp_to_next_level = int((.04 * (lvl ** 3) + .8 * (lvl ** 2) + 2 * lvl) + 100)

                 # check if a level up has occured 
                if exp >= exp_to_next_level: 
                    # increment the level for the user 
                    await self.bot.db.execute('''
                    UPDATE levelData 
                    SET lvl = lvl + 1 
                    WHERE guild_id = ? AND user_id = ?
                    ''', (message.guild.id, message.author.id))

                    # reset the exp 
                    await self.bot.db.execute('''
                    UPDATE levelData
                    SET exp = 0
                    WHERE guild_id = ? AND user_id = ?
                    ''', (message.guild.id, message.author.id))

                    new_level = lvl + 1


                    # alert user of level up 
                    await message.channel.send(f'{message.author.mention} Congrats!! You are now level **{new_level}!!!**')
            await self.bot.db.commit()


    @commands.command(name='lvl', help='Displays a users level.')
    async def level(self, ctx, member: discord.Member = None): 
        if member is None: 
            member = ctx.author

        # FETCH DATA FROM DB
        async with self.bot.db.execute('SELECT exp, lvl, msg_count  FROM levelData WHERE guild_id = ? AND user_id = ?', (ctx.guild.id, member.id)) as cursor: 
            data = await cursor.fetchone()
            curr_exp = data[0] 
            lvl = data[1] 
            msg_count = data[2]
        
        exp_to_next_level = int((.04 * (lvl ** 3) + .8 * (lvl ** 2) + 2 * lvl) + 100) 
        # embed that shows information about the level stats of the requwsted user 
        embed = discord.Embed(title='Level Stats', description=f'Level stats for the server {ctx.guild.name}', color=member.color)
        embed.set_author(name=f'{ctx.author.name}#{ctx.author.discriminator}', icon_url=member.avatar_url)
        embed.set_thumbnail(url=member.avatar_url)
        embed.add_field(name='Amount of messages sent: ', value=msg_count, inline=False)
        embed.add_field(name='Current Level:', value=f'**{lvl}**', inline=True)
        embed.add_field(name='**Experience**: ', value=f'{curr_exp}/ {exp_to_next_level}')

        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Level(bot)) 