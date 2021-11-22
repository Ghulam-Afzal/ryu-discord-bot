from discord import embeds
from discord.ext import commands
import discord 

class Shop(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot 
        self.shop = {"car": 30000, "house": 450000, "cat": 5000, "dog": 5000, "mansion": 1000000} 
        
        
        
    @commands.command(name="plist")
    async def list_purchasble_items(self, ctx):
         
        embed = discord.Embed(title="SHOP")
         
        for item in self.shop:
            embed.add_field(name=f"{item}", value=f"The price of this item is {self.shop[item]}", inline=False)
             
        await ctx.send(embed=embed)
        return 
    
    @commands.command()
    async def purchase(self, ctx, *, item):
        pass
    
    
def setup(bot):
    bot.add_cog(Shop(bot))