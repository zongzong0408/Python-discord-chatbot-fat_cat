"""
    講垃圾話、幹話、廢圖、梗圖的程式
"""
import discord as dc
from discord.ext import commands
# import discord_ui as dc_ui                    # 不可引用，會報錯
from Core import Cog_Extension

import random
import json
import requests as req

class Say(Cog_Extension):

    """
        想做下拉式選單，不可執行，編譯器報錯。
        原因好像是版本不配合，應該要用 python2 配合 discord.ui(discord_ui ?)
    """
    # @commands.command()
    # async def mood(self, ctx):
    #     select = dc_ui.SelectInteraction(
    #         option = [
    #             dc_ui.SelectOption(label = "Cloudy", emoji = "⛅", description = "cloudy weather"),
    #             dc_ui.SelectOption(label = "running", emoji = "🌧", description = "running weather")
    #         ]
    #     )

    #     await ctx.send("Choose a weather !", dc_ui.components = select)

    @commands.command(aliases = ["p-i"])
    async def show_funny_picture_information(self, ctx):
        """
            Shows ./show_funny_picture 's usage.
        """
        embed = dc.Embed(
            title = "funny picture introduce",
            description = "\
                __./show_funny_picture_information__ 's Hot Key : p-i\n\
                __./show_funny_picture__ 's Hot Key : p-s\n\
                ",
            color = 0xff955a
        )

        await ctx.send(embed = embed)

    @commands.command(aliases = ["p-s"])
    async def show_funny_picture(self, ctx):
        """
            Shows funny meme(just for fun 😘).
        """
        # try:

        with open("./database.json", "r", encoding = "utf-8") as file:
            data = json.load(file)
        # print(data)
        
        random_pic = random.choice(data["funny_picture"])
        # print(random_pic)
        
        # 確認連結是否正確 
        request = req.get(url = random_pic)
        
        if request.status_code == 200:

            await ctx.send(random_pic)
        
        else:

            await ctx.send("error")


def setup(bot):
    bot.add_cog(Say(bot))