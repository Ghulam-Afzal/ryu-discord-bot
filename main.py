import os
import logging
import discord 
import aiosqlite
import asyncio
from dotenv import load_dotenv
from discord.ext import commands 


# set up logging for the bot 
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter((logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s')))
logger.addHandler(handler)

# load enviroment vars 
load_dotenv() 
TOKEN = os.getenv("TOKEN")

# set up member intents and the command prefix for the bot 
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

async def initialize():
    await bot.wait_until_ready()

    bot.db = await aiosqlite.connect('ryu.db')
    await bot.db.execute("CREATE TABLE IF NOT EXISTS economyTable (guild_id int, user_id int, job text, wallet int, bank int, PRIMARY KEY (guild_id, user_id))")
    await bot.db.execute("CREATE TABLE IF NOT EXISTS levelData (guild_id int, user_id int, lvl int, exp int, msg_count int, PRIMARY KEY (guild_id, user_id))")
    await bot.db.execute("CREATE TABLE IF NOT EXIsTS shopData (guild_id int, user_id int, items longtext, PRIMARY KEY (guild_id, user_id))")


if __name__ == '__main__':
    for filename in os.listdir("./cogs"):
        if filename.endswith('.py'):
            try: 
                cog_loaded = filename.replace(".py", "")
                bot.load_extension(f'cogs.{filename[:-3]}')
                print(cog_loaded)
            except Exception as e: 
                print(e)

bot.loop.create_task(initialize())
bot.run(TOKEN)
asyncio.run(bot.db.close())