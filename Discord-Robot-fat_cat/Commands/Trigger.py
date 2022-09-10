"""
    Event
    觸發事件的程式
"""
import discord as dc
from discord.ext import commands
import os
from Core import Cog_Extension

class Trigger(Cog_Extension):
    # 成員進入，歡迎訊息
    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = self.bot.get_channel(int(os.getenv("member_channel")))
        await channel.send(f"Welcome @{member} 's join! ❤ 😍 😁 💕")

    # 成員退出，不捨訊息
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = self.bot.get_channel(int(os.getenv("member_channel")))
        await channel.send(f"Sad about @{member} 's leaving... 😢 😒 🤢 🌹")

    # 向不熟的使用者介紹使用方式
    @commands.Cog.listener()
    async def on_message(self, msg):

        Help = ["help", "Help"]
        Command = ["./help"]

        for word in Help:
            if msg.content.find(word) >= 0 and msg.author != self.bot.user and msg.content not in Command:
                embed = dc.Embed(
                    title = "幫助訊息 Help Information",
                    description = 
                    "**請輸入 ./help 以獲得更多資訊 😘\nPlease input __./help__ to see more information.**\
                    \n\n指令前須加入<__./__>前綴詞才可激發**__肥肥貓__**執行該指令\n\
                    \n\n可輸入__./introduce__獲得全部詳細指令資訊\n\n若有遇到任何 Bug 可輸入 __./developer__ 聯絡開發人員 🐱‍💻 🤞\
                    \n此專案為開源專案，程式碼皆公布在 GitHub 上\nlink : __https://github.com/zongzong0408/Discord-Robot-fat_cat__\n\n\
                    為綠色軟體，請安心服用。 ✨ 👌 ✨ \
                    ",
                    color = 0x7E3D76
                )
                await msg.channel.send(embed = embed)


def setup(bot):
    bot.add_cog(Trigger(bot))