from discord.ext import commands


class Utils(commands.Cog):
    def __init__(self, bot):
        self.bot = bot 


    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            seconds = error.retry_after % (24 * 3600)
            hour = seconds // 3600
            seconds %= 3600
            minutes = seconds // 60
            seconds %= 60
            time =  "%d:%02d:%02d" % (hour, minutes, seconds)

            msg = f"You are still on cooldown {time}"
            await ctx.send(msg)


def setup(bot):
    bot.add_cog(Utils(bot))