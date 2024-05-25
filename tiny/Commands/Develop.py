"""
    新功能開發的測試區
"""
import discord as dc
from discord.ext import commands
from Core import Cog_Extension

class Develop(Cog_Extension):
    
    @commands.command(aliases = ["t"])
    async def test(self, ctx):
        """
            Hello World!
        """

        await ctx.send("Hello World!")    

def setup(bot):
    bot.add_cog(Develop(bot))