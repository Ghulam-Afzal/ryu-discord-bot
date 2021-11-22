from discord.ext import commands


class Shop(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot 
        
        
        
    @commands.command(name="plist")
    async def list_purchasble_items(self, ctx):
        pass 
    
    @commands.command()
    async def purchase(self, ctx, *, item):
        pass 
    
    
def setup(bot):
    bot.add_cog(Shop(bot))