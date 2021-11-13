import random
from discord.ext import commands
import aiosqlite

class Level(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    

    @commands.Cog.listener()
    async def on_message(self, message):
        '''     
            idk how else to make this work
            So for now this will be my solution
            atleast until I find a better way to 
            connect to the db 
        '''
        db = await aiosqlite.connect("ryu.db")
        if not message.author.bot: 
            cursor = await db.execute('''
            INSERT OR IGNORE INTO levelData 
            (guild_id, user_id, lvl, exp, msg_count)
            VALUES(?,?,?,?,?)
            ''', (message.guild.id, message.author.id, 1, 0, 0))

            if cursor.rowcount == 0: 
                exp_given = random.randint(15, 25)
                await db.execute('''
                UPDATE levelData 
                SET exp = exp + ? 
                WHERE guild_id = ? AND user_id = ?
                ''', (exp_given, message.guild.id, message.author.id))

                await db.execute('''
                UPDATE levelData 
                SET msg_count = msg_count + 1 
                WHERE guild_id = ? AND user_id = ?
                ''', (message.guild.id, message.author.id))

                cur = await db.execute('''
                SELECT exp FROM levelData
                WHERE guild_id = ? AND user_id = ?
                ''', (message.guild.id, message.author.id))

                curr_lvl = await db.execute('''
                SELECT lvl FROM levelData 
                WHERE guild_id = ? AND user_id = ?
                ''', (message.guild.id, message.author.id))
                data = await cur.fetchone() 
                exp = data[0]
                temp = await curr_lvl.fetchone()
                lvl = temp[0]
                print(lvl)

                # calc exmp required for next level and then update the 
                exp_to_next_level = int((.04 * (lvl ** 3) + .8 * (lvl ** 2) + 2 * lvl) + 100)

                 # check if a level up has occured 
                if exp >= exp_to_next_level: 
                    # increment the level for the user 
                    await db.execute('''
                    UPDATE levelData 
                    SET lvl = lvl + 1 
                    WHERE guild_id = ? AND user_id = ?
                    ''', (message.guild.id, message.author.id))

                    # reset the exp 
                    await db.execute('''
                    UPDATE levelData
                    SET exp = 0
                    WHERE guild_id = ? AND user_id = ?
                    ''', (message.guild.id, message.author.id))

                    new_level = lvl + 1
            

                    # alert user of level up 
                    await message.channel.send(f'{message.author.mention} Congrats!! You are now level **{new_level}!!!**')
            await db.commit()

        await self.bot.process_commands(message)

def setup(bot):
    bot.add_cog(Level(bot))