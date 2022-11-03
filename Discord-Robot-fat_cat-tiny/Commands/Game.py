"""
    玩遊戲的程式
"""
import discord as dc
from discord.ext import commands
from Core import Cog_Extension

import random
import time

class Game(Cog_Extension):
    """
        Global Variable
    """
    # One A Two B Game's Global Variable
    global oneAtwoB_START
    global oneAtwoB_Answer
    global oneAtwoB_Ranking
    global oneAtwoB_UsingTime
    global start_time
    global end_time

    oneAtwoB_START = False
    start_time = end_time = 0.0

    oneAtwoB_Answer = random.sample(range(1, 10), 4)
    print(f"robot : this oneAtwoB round's answer is : {oneAtwoB_Answer}")
    
    oneAtwoB_Ranking = []
    oneAtwoB_UsingTime = {}

    """
        Function
    """
    @commands.command(aliases = ["g-i"])
    async def oneAtwoB_introduce(self, ctx) -> None:
        """
            Shows ./oneAtwoB_introduce 's usage.
            Hot Key : g-i
        """
        # await ctx.send("One-A-Two-B will show in channel : <game_channel>")

        embed = dc.Embed(
            title = " 🎮 One A Two B Game Introduce",
            description = "**1A2B 指令說明**",
            color = 0x2894FF)
        embed.add_field(
            name = "遊戲流程說明：",
            value = 
            "第一次輸入：需要輸入 Start 或 S 或 s 來開始遊戲(開始計時)\
            \n第二次輸入：如下 輸入範例 Example Input & 遊戲範例 Example Play\n\n\
            __./oneAtwoB_introduce__ 's Hot Key : g-i\n\
            __./oneAtwoB__ 's Hot Key : g-s\n\
            ",
            inline = False)
        embed.add_field(
            name = "輸入範例 Example Input",
            value = 
            "指令：./oneAtwoB 1234 \
            \n說明：輸入 1234\
            \n\n指令：./oneAtwoB Rank (或 rank 或 R 或 r)\
            \n說明：直接呼叫目前的排行榜\
            \n\n指令：./oneAtwoB Exit (或 exit 或 End 或 end 或 E 或 e)\
            \n說明：直接退出遊戲(沒有破關的紀錄會沒有存檔)\n",
            inline = False)
        embed.add_field(
            name = "遊戲範例 Example Play (1)",
            value = 
            "**Input —> 1111\
            \nResult —> 0 A 2 B**",
            inline = False)
        embed.add_field(
            name = "遊戲範例 Example Play (2)",
            value = 
            "**Input —> 9487\
            \nResult —> 2 A 2 B**",
            inline = False)

        await ctx.send(embed = embed)

    @commands.command(aliases = ["g-s"])
    async def oneAtwoB(self, ctx):
        """
            Play 1A2B game on discord.
            Hot Key : g-s

            玩 1A2B 遊戲。
        """
        global oneAtwoB_START                   # 遊戲是否開啟進行
        global oneAtwoB_Answer                  # 玩家是否回答正確
        global oneAtwoB_Ranking                 # 玩家排行榜(越快回答正確答案，排名越高)
        global oneAtwoB_UsingTime               # 玩家遊戲時間(中途退出和回答正確時才會停止計時)
        global start_time                       # 開始遊戲時間
        global end_time                         # 結束遊戲時間

        # 函式：記分板(Ranking Board) 排序、製作、顯示
        async def show_ranking() -> None:
            oneAtwoB_Ranking = sorted(oneAtwoB_UsingTime.items(), key = lambda x : x[1])

            result_embed = dc.Embed(
                title = "One A Two B Ranking Table",
                color = 0x2894FF
            )
            for user in oneAtwoB_Ranking:
                result_embed.add_field(
                    name = f"Name : **{user[0]}**",
                    value = f"Cost : **{round(time.localtime(user[1]).tm_sec, 2)} s**",
                    inline = False
                )
            # print(len(result_embed))
            # 用長度去判斷 embed 為 Empty 時，長度為多少，再進行判斷
            if len(result_embed) <= 25:
                embed = dc.Embed(
                    description = "The Ranking Board is not record yet.",
                    color = 0x2894FF
                )
                await ctx.send(embed = embed)
            else:
                await ctx.send(embed = result_embed)

        # 避免輸入者為機器人，造成無限迴圈(機器人發話後又觸發一次程式，造成重複)
        if ctx.author == self.bot.user:
            return

        # 獲取使用者訊息
        get_msg = ctx.message.content
        msg = "" + get_msg[11 : len(get_msg)]

        if msg == "g-s show ans":
            await ctx.send(f"This oneAtwoB round's answer is : {oneAtwoB_Answer}")

        # 查看排行榜
        Rank = ["Rank", "rank", "R", "r"]

        for word in Rank:
            if word == msg:
                rank_embed = dc.Embed(
                    description = "Has been showed One A Two B game successfully.",
                    color = 0x2894FF
                )
                await ctx.send(embed = rank_embed)

                await show_ranking()
            
                return

        if oneAtwoB_START == False:
            if msg == "Start" or msg == "S" or msg == "s":
                oneAtwoB_START = True
                start_time = time.time()

                embed = dc.Embed(
                    description = "Game is starting & counting now",
                    color = 0x2894FF
                )
                await ctx.send(embed = embed)
                
                return
            else:
                embed = dc.Embed(
                    description = "The first game round must start by input \"Start\" or \"S\" or \"s\"",
                    color = 0x2894FF
                )
                await ctx.send(embed = embed)
        
        if oneAtwoB_START == True:
            # 遊戲中中途離開
            Exit = ["Exit", "exit", "End", "end", "E", "e"]

            for word in Exit:
                if word == msg:
                    exit_embed = dc.Embed(
                        description = "Has been exited One A Two B Ranking Table successfully.",
                        color = 0x2894FF
                    )
                    await ctx.send(embed = exit_embed)

                    oneAtwoB_START = False

                    return

            # 獲取使用者名稱
            get_name = ctx.message.author
            name = get_name.name

            n1 = n2 = n3 = 0

            # 不是 4A0B 的狀況
            input = list()
            input = msg

            for i in input:
                if int(input[n1]) == oneAtwoB_Answer[n1]:
                    n1 = n1 + 1
                else:
                    if int(i) in oneAtwoB_Answer:
                        n2 = n2 + 1
                n3 = n3 + 1
            
            # output = ",".join(input).replace(",","")

            # 紀錄完成時間
            end_time = time.time()
            # print(end_time, start_time)

            if ctx.author not in oneAtwoB_UsingTime:
                oneAtwoB_UsingTime[name] = end_time - start_time
            else:
                if end_time - start_time < oneAtwoB_UsingTime[name]:
                    oneAtwoB_UsingTime[name] = end_time - start_time
            
            round_embed = dc.Embed(
                title = f"Input   —> {msg}\nResult —> {n1} A {n2} B",
                color = 0x2894FF
            )
            await ctx.send(embed = round_embed)

            # 是 4A0B 的狀況，答案正確
            if n1 == 4:
                if ctx.author not in oneAtwoB_UsingTime:
                    oneAtwoB_UsingTime[name] = end_time - start_time
                else:
                    if end_time - start_time < oneAtwoB_UsingTime[name]:
                        oneAtwoB_UsingTime[name] = end_time - start_time
                
                await ctx.send(f"**You got the correct answer ! The answer is {oneAtwoB_Answer}**")
                await ctx.send(f"**It took you {round(time.localtime(oneAtwoB_UsingTime[name]).tm_sec, 2)} scends to complete.**")

                await show_ranking()

                oneAtwoB_Answer = random.sample(range(1, 10), 4)
                print(f"robot : this oneAtwoB round's answer is : {oneAtwoB_Answer}")
                oneAtwoB_START = False


def setup(bot):
    bot.add_cog(Game(bot))