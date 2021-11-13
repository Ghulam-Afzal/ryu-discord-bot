from discord.ext import commands
import discord


class Misc(commands.Cog):

    def __init__(self, bot):
        self.bot = bot 

    @commands.command()
    async def show_avatar(self, ctx, *, member: discord.Member = None):
    # if there was no user specified then return the avatar of the message author
        if member is None:
            name = ctx.author.name
            show_av = discord.Embed(

                title=name,
                color=discord.Color.dark_blue()
            )
            show_av.set_image(url=f'{ctx.author.avatar_url}')
            await ctx.send(embed=show_av)
        # if the member was specified then return the avatar of the
        else:
            name = member.name
            show_av = discord.Embed(

                title=name,
                color=discord.Color.dark_blue()
            )
            show_av.set_image(url=f'{member.avatar_url}')
            await ctx.send(embed=show_av)

def setup(bot):
    bot.add_cog(Misc(bot))