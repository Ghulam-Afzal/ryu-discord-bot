from discord.ext import commands


class TestExample(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self.bot.user.name} is ready')


def setup(bot):
    bot.add_cog(TestExample(bot))
