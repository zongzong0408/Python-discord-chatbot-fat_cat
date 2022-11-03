"""
    存放一些重要東西的程式(跟開發後端比較有關係)
"""
import discord as dc
from discord.ext import commands
import os
from Core import Cog_Extension

import datetime

class Main(Cog_Extension):

    @commands.command(aliases = ["w"])
    async def welcome(self, ctx):
        """
            Let "fat cat" welcomes you again.
        """
        await ctx.send(f"Hello, @{ctx.author} !")

    # can show in local shell
    @commands.command(aliases = ["e"])
    async def echo(self, ctx, *msg):
        """
            Shows words in local shell.
        """
        
        remove = ["(", ")", ","]
        msg_r = list()
        msg_c = list(msg)
        
        for e in msg_c:
            if e not in remove:
                msg_r.append(e)
        message = "".join(msg_r)

        await ctx.send(message)
        os.system(f"echo {message}")
    
    @commands.command()
    async def cls(self, ctx):
        """
            Work as same as cls in local shell.
        """
        os.system("cls")
        
        await ctx.send("fully completed.")

    @commands.command(aliases = ["d"])
    async def developer(self, ctx):
        """
            Show "fat cat" developer.
        """
        
        embed = dc.Embed(
            title = "AI Discord Robot Developer",
            url = "https://discord.com/api/oauth2/authorize?client_id=988002605068353587&permissions=534727096384&scope=bot",
            description = "開發 AI Discord Robot 的人員",
            color = 0xfcd7d6, 
            timestamp = datetime.datetime.now()
        )
        embed.set_author(
            name = "zong zong",
            url = "https://github.com/zongzong0408",
            icon_url = "https://i.pinimg.com/originals/43/f0/5b/43f05bff9062461590bef9043ba77929.jpg"
        )
        embed.set_thumbnail(
            url = "https://i.pinimg.com/originals/67/29/fc/6729fc2f0f62c0ea5784ee66c9595a2f.jpg"
        )
        embed.add_field(
            name = "**IG**",
            value = "chu__0408\_",
            inline = True
        )
        embed.add_field(
            name = "**Email**",
            value = "zongzongchu0408@gmail.com",
            inline = False
        )
        embed.add_field(
            name = "**GitHub : 肥肥貓**",
            value = "https://github.com/zongzong0408/Discord-Robot-fat_cat",
            inline = False
        )
        embed.set_footer(text = "Date : 2022/07/03")
        
        await ctx.send(embed = embed)


def setup(bot):
    bot.add_cog(Main(bot))