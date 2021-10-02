import os
import discord 
from discord.ext import commands 


bot = commands.Bot(command_prefix="!")



if __name__ == '__main__':
    for ext in os.listdir("./cogs"):
        bot.load_extension(ext)

bot.run("ODkyOTU2MTY4MDE4ODc4NTA2.YVUcPA.6P3tdg3vQAuo1ppRqVETuHaDCsY")