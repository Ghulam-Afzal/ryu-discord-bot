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
        if item is None: 
            await ctx.send("A item to purchase needs to be specified.")
            # TODO: make the table have multiple columns where that use a  true false value to show whether the person owns something or not. 
        else: 
            if item in self.shop:
                cursor = await self.bot.db.execute("SELECT items WHERE guild_id = ? AND user_id = ?", (ctx.guild.id, ctx.author.id))
                result = await cursor.fetchone()
                
                if result is None:
                    lst = []
                    lst.append(item)
                    temp = str(lst)
                    await self.bot.db.execute("UPDATE items WHERE guild_id = ? AND user_id = ?", (temp, ctx.guild.id, ctx.author.id))        
                
                else:
                    temp1 = list(result[0])
                    temp1.append(item)
                    temp2 = str(temp1)
                    await self.bot.db.execute("UPDATE items WHERE guild_id = ? AND user_id = ?", (temp2, ctx.guild.id, ctx.author.id))
                    return 
                
                await ctx.send(f"You have purchased {item}")   
                return 
            
            else: await ctx.send(f"{item} is not up for purchase.")  
    
    
def setup(bot):
    bot.add_cog(Shop(bot))