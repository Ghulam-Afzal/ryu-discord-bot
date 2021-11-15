from discord.ext import commands
import discord
import requests
import random 


class Misc(commands.Cog):

    def __init__(self, bot):
        self.bot = bot 
        self.list_of_qoutes = []

        r = requests.get('https://type.fit/api/quotes')
        data = r.json()

        for i in data:
            self.list_of_qoutes.append(i)

        

    @commands.command(aliases=['av', 'avatar', 'AV', 'Av', 'AVATAR'], help='Shows your avatar.')
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


    @commands.command(aliases=['quote', 'randomquote', 'qu'], help='Responds with a random quote')
    async def quote_gen(self, ctx):
        random_index = random.randint(0, (len(self.list_of_qoutes) - 1))
        quote = f'"{self.list_of_qoutes[random_index]["text"]}" - {self.list_of_qoutes[random_index]["author"]}'
        await ctx.send(quote)


    @commands.command(name='ping', help='Shows the ping.')
    async def show_ping(self, ctx):
        p = round(self.bot.latency, 4) * 1000
        await ctx.send(f'{p}ms')

def setup(bot):
    bot.add_cog(Misc(bot))