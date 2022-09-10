"""
    間隔一段時間執行命令
"""

import discord as dc
from discord.ext import commands
from discord.ext import tasks
import os
from Core import Cog_Extension

import urllib.request as req
import bs4

CWB_earthquake_file_url = "https://www.cwb.gov.tw/V8/C/E/MOD/MAP_LIST.html?T=2022082817-2"

global CWB_titles
global CWB_titles_new
global CWB_count                                # 紀錄 robot 偵測及時地震發生次數

CWB_titles = [[' ' for i in range(7)] for j in range(15)]
CWB_titles_new = [[' ' for i in range(7)] for j in range(15)]
CWB_count = 0

def CWB_earthquake_crawling(array: list) -> None:

    web_request = req.Request(CWB_earthquake_file_url, headers = 
    {
        "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"
    })

    with req.urlopen(url = web_request) as response:
        web_data = response.read().decode("utf-8")
    
    web_fitter = bs4.BeautifulSoup(web_data, "html.parser")


    web_dot = web_fitter.find_all("a", class_ = "dot")
    web_far_dot = web_fitter.find_all("a", class_ = "far-dot")

    for target in web_dot:

        data_name = str(target["data-name"])
        number = "" + data_name[3 : ]
        number = int(number)

        array[number - 1][0] = str(number)
        array[number - 1][1] = str(target.string)

    try:

        for target in web_far_dot:
            
            data_name = str(target["data-name"])
            number = "" + data_name[3 : ]
            number = int(number)

            array[number - 1][0] = str(number)
            array[number - 1][1] = str(target.text)
            # print(array[number - 1][1]) 

    except:

        pass

    for i in range(0, 15, 1):
        
        words = array[i][1].split("，")

        if words[0] != "None":
            
            array[i][2] = words[0]
            array[i][3] = words[1]
            array[i][4] = words[2]
            array[i][5] = words[3]
            array[i][6] = words[4]

    return 

def CWB_earthquake_make_embed(array: list, start: int, end : int):
            
    embed = dc.Embed(
        title = " 🌋 交通部中央氣象局——最近地震 標題",
        description = "CWB Board Title",
        color = 0xFF5733
    )
    for i in range(start, end, 1):

        embed.add_field(
            name = f"地震時間：{array[i][3]}",
            value = f"\
                形成地點：{array[i][4]}\n\
                影響區域：{array[i][2]}\n\
                地震規模：**{array[i][6]}**\n\
                地震深度：{array[i][5]}\n\
                地震編號：__{array[i][0]}__\n\n\n\
                ",
            inline = False
        )

    return embed

class Routine(Cog_Extension):

    def __init__(self, *args):
        super().__init__(*args)
        # self.peanuts.start()
        self.detect_earthquake.start()

    '''
    @tasks.loop(seconds = 20.0)
    async def peanuts(self):

        await self.bot.wait_until_ready()
        self.channel = self.bot.get_channel(int(os.getenv("general_channel")))
        await self.channel.send("Peanuts !")
    '''

    @tasks.loop(seconds = 2.0)
    async def detect_earthquake(self):
        """
            Auto detects CWB currently earthquakes. (loop 2.0s)

            自動 偵測 交通部中央氣象局-最近地震 標題。
        """
        """
            Web URL = https://www.cwb.gov.tw/V8/C/E/index.html
            Document URL = https://www.cwb.gov.tw/V8/C/E/MOD/MAP_LIST.html?T=2022082817-2
            Target = HTML XHR titles
        """
        
        await self.bot.wait_until_ready()

        global CWB_titles
        global CWB_titles_new
        global CWB_count

        start = -1
        end = -1
        
        channel = self.bot.get_channel(int(os.getenv("main_channel")))

        # Function Start

        CWB_earthquake_crawling(CWB_titles_new)

        different = 0

        # 偵測是否資料更新
        for i in range(15):
            for j in range(7):
                
                if CWB_titles[i][j] != CWB_titles_new[i][j]:
                    if start == -1:

                        different += 1
                        start = i
                        
                else:
                    if end == -1:
                        
                        end = i

            if start != -1 and end != -1:

                break
        #
            
            if different == 0:

                # await channel.send("")

                if CWB_count == 0:
                    CWB_count += 1
            
            else:
                if CWB_count != 0:

                    CWB_earthquake_crawling(CWB_titles)

                    await channel.send(embed = CWB_earthquake_make_embed(CWB_titles_new, start, end))

                    CWB_count += 1
                    print(CWB_count - 1) 


def setup(bot):
    bot.add_cog(Routine(bot))