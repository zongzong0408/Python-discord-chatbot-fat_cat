"""
    爬蟲的程式
"""
import discord as dc
from discord.ext import commands
import os
from Core import Cog_Extension

import urllib.request as req
import bs4
import time

CWB_LIMIT = 100

# URL
ptt_movie_url = "https://www.ptt.cc/bbs/movie/index.html"
ptt_gossip_url = "https://www.ptt.cc/bbs/Gossiping/index.html"
CWB_earthquake_file_url = "https://www.cwb.gov.tw/V8/C/E/MOD/MAP_LIST.html?T=2022082817-2"

"""
    Global Variable
"""
global ptt_movie_newest_url
global ptt_movie_now_url
global ptt_movie_page
global ptt_movie_now_page

global ptt_gossip_newest_url
global ptt_gossip_now_url
global ptt_gossip_page
global ptt_gossip_now_page

# 初始化
ptt_movie_newest_url = ""
ptt_movie_page = 0

ptt_gossip_newest_url = ""
ptt_gossip_page = 0

# 函式 : 取得最新網址的前一頁
def get_url(cmd : int, url : str) -> str:

    # PTT movie
    if cmd == 1:
        """
            url connect
        """
        web_request = req.Request(url, headers = 
        {
            "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
        })

        with req.urlopen(url = web_request) as response:
            web_data = response.read().decode("utf-8")
        # print(web_data)

        web_fitter = bs4.BeautifulSoup(web_data, "html.parser")
        # print(web_fitter.title.string)

        """
            take target
        """
        web_forward_address = web_fitter.find("a", string = "‹ 上頁")
        web_address = str(web_forward_address["href"])
        # print(web_address)

        newest_url = "https://www.ptt.cc/" + web_forward_address["href"]

        page = ""

        for i in range(len(web_address)):
            if web_address[i].isdigit() == True:
                if page == "":
                    page = "" + web_address[i]
                else:
                    page += str(web_address[i])
        # print(page)

        return [newest_url, page]
    
    # PTT Gossiping
    elif cmd == 2:

        web_request = req.Request(url, headers = 
        {
            "cookie" : "over18=1",
            "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
        })
        
        with req.urlopen(url = web_request) as response:
            web_data = response.read().decode("utf-8")
        # print(web_data)

        web_fitter = bs4.BeautifulSoup(web_data, "html.parser")
        # print(web_fitter.title.string)

        """
            take target
        """
        web_forward_address = web_fitter.find("a", string = "‹ 上頁")
        web_address = str(web_forward_address["href"])
        # print(web_address)

        newest_url = "https://www.ptt.cc/" + web_forward_address["href"]

        page = ""

        for i in range(len(web_address)):
            if web_address[i].isdigit() == True:
                if page == "":
                    page = "" + web_address[i]
                else:
                    page += str(web_address[i])
        # print(page)

        return [newest_url, page]

# e.g. ptt_movie_newest_url = https://www.ptt.cc//bbs/movie/indexXXXX.html
ptt_movie_newest_url = get_url(1, ptt_movie_url)[0]
ptt_movie_page = "" + get_url(1, ptt_movie_url)[1]
ptt_movie_page = int(ptt_movie_page)

ptt_movie_now_url = ptt_movie_newest_url
ptt_movie_now_page = ptt_movie_page
# print(ptt_movie_page, ptt_movie_now_page)

ptt_gossip_newest_url = get_url(2, ptt_gossip_url)[0]
ptt_gossip_page = "" + get_url(2, ptt_gossip_url)[1]
ptt_gossip_page = int(ptt_gossip_page)

ptt_gossip_now_url = ptt_gossip_newest_url
ptt_gossip_now_page = ptt_gossip_page

class Crawler(Cog_Extension):    

    @commands.command(aliases = ["c-ptt-m-i"])
    async def check_ptt_movie_information(self, ctx):
        """
            Shows ./check_ptt_movie 's usage.
            Hot Key : ./c-ptt-m-i
        """
        embed = dc.Embed(
            title = " 🔎🐍 Check ptt movie Board Title Information",
            description = "\
                ptt movie 看板 標題 爬蟲 使用說明\n\n\
                ./check_ptt_movie_information 's Hot Key : ./c-ptt-m-i\n\
                ./check_ptt_movie 's Hot Key : ./c-ptt-m-s\n\
                ",
            color = 0xFF5733
        )
        embed.add_field(
            name = "./check_ptt_movie(or ./c-ptt-m-s)",
            value = f"爬取 ptt movie 的最新一頁的前一頁",
            inline = False
        )
        embed.add_field(
            name = "./check_ptt_movie > (or ./c-ptt-m-s >)",
            value = f"爬取 ptt movie 的下一頁",
            inline = False
        )
        embed.add_field(
            name = "./check_ptt_movie < (or ./c-ptt-m-s <)",
            value = f"爬取 ptt movie 的上一頁",
            inline = False
        )
        embed.add_field(
            name = "./check_ptt_movie_information(or ./c-ptt-m-i)",
            value = f"查看 __./check_ptt_movie__ 功能和如何使用",
            inline = False
        )

        await ctx.send(embed = embed)

    @commands.command(aliases = ["c-ptt-m-s"])
    async def check_ptt_movie(self, ctx):
        """
            Crawling ptt movie board's titles.
            Hot Key : ./c-ptt-m-s

            爬取 PTT 電影版 標題。
        """
        """
            Web URL = https://www.ptt.cc/bbs/movie/index.html
            Target = HTML movie titles
        """
        # string class -> <class 'bs4.element.NavigableString'>
        
        # ptt movie 版，一頁最多 20 則討論
        # 宣告一個 20 * 3 的二維陣列
        """
            [ ][0] : 存放標題
            [ ][1] : 存放連結
            [ ][2] : 存放時間
        """
        ptt_titles = [[' ' for i in range(3)] for i in range(20)]

        global ptt_movie_newest_url
        global ptt_movie_now_url
        global ptt_movie_page
        global ptt_movie_now_page

        # 函式：接收使用者輸入並過濾指令提式與語，傳回字串
        def ptt_movie_input() -> str:

            if ctx.author == self.bot.user:
                return
            else:
                # 獲取輸入訊息
                get_msg = ctx.message.content
                msg = ""
            
                # 過濾開頭指令提示語
                if ("" + get_msg[0 : 18]) == "./check_ptt_movie ":
                    msg = "" + get_msg[18 : len(get_msg)]
                elif ("" + get_msg[0 : 12]) == "./c-ptt-m-s ":
                    msg = "" + get_msg[12 : len(get_msg)]

                return msg

        # 函式：開始爬蟲
        def crawling(cmd : str, url : str) -> str:

            web_request = req.Request(url, headers = 
            {
                "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
            })

            with req.urlopen(url = web_request) as response:
                web_data = response.read().decode("utf-8")
            
            web_fitter = bs4.BeautifulSoup(web_data, "html.parser")


            web_titles = web_fitter.find_all("div", class_ = "title")
            
            times = 0
            for target in web_titles:
                if target.a != None:
                    # await ctx.send(target.a.string)
                    ptt_titles[times][0] = str(target.a.string)
                    ptt_titles[times][1] = str(target.a["href"])

                    times += 1
            
            web_date = web_fitter.find_all("div", class_ = "date")
            
            times = 0
            for target in web_date:
                if target != None:
                    ptt_titles[times][2] = str(target.string)

                    times += 1

            if cmd == '>':
            
                pass_url = web_fitter.find("a", string = "下頁 ›")

                return str("https://www.ptt.cc/" + pass_url["href"])
            
            elif cmd == '<':

                pass_url = web_fitter.find("a", string = "‹ 上頁")

                return str("https://www.ptt.cc/" + pass_url["href"])

            return url

        # 函式：製作 Embed
        def make_embed():

            embed = dc.Embed(
                title = " 💬 ptt movie Board Title",
                description = "ptt movie 看板 標題",
                color = 0xFF5733
            )
            for i in range(20):

                if ptt_titles[i][0] != ' ' and ptt_titles[i][1] != ' ' and ptt_titles[i][2] != ' ':

                    embed.add_field(
                        name = f"{ptt_titles[i][0]}",
                        value = f"\
                            __{ptt_titles[i][1]}__\n\
                            **{ptt_titles[i][2]}**\
                            ",
                        inline = False
                    )

            embed.add_field(
                name = "Page 頁數",
                value = f"page : {ptt_movie_now_page}",
                inline = False
            )
            
            return embed

        user_input = ptt_movie_input()
        # print(f"user_input : {user_input}")

        if user_input == "":

            ptt_movie_now_url = crawling('0', ptt_movie_newest_url)

            await ctx.send(embed = make_embed())
        
        elif user_input == '>':
            
            ptt_movie_now_page += 1
            
            if ptt_movie_now_page == ptt_movie_page + 1:
                ptt_movie_now_page = 0
            
            url = "https://www.ptt.cc/bbs/movie/index" + str(ptt_movie_now_page) + ".html"

            try:

                crawling('0', url)
                # ptt_movie_now_url = crawling('>', ptt_movie_now_url) 

                await ctx.send(embed = make_embed())
            
            except:

                embed = dc.Embed(
                    title = "❌ Sorry : error web url",
                    description = "Please tell the developer this error situation.(the target url must be changed.)",
                    color = 0x7E3D76
                )

                await ctx.send(embed = embed)

        elif user_input == '<':

            if ptt_movie_now_page == 0:
                ptt_movie_now_page = ptt_movie_page + 1

            ptt_movie_now_page -= 1

            url = "https://www.ptt.cc/bbs/movie/index" + str(ptt_movie_now_page) + ".html"

            try:

                crawling('0', url)
                # ptt_movie_now_url = crawling('<', ptt_movie_now_url)

                await ctx.send(embed = make_embed())
            
            except:

                embed = dc.Embed(
                    title = "❌ Sorry : error web url",
                    description = "Please tell the developer this error situation.(the target url must be changed.)",
                    color = 0x7E3D76
                )

                await ctx.send(embed = embed)
        
        else:
            
            embed = dc.Embed(
                title = "❌ Sorry : error input",
                description = "Please go to check command information to know how to use.",
                color = 0x7E3D76
            )

            await ctx.send(embed = embed)
    
    @commands.command(aliases = ["c-ptt-g-i"])
    async def check_ptt_gossiping_information(self, ctx):
        """
            Shows ./check_ptt_gossiping 's usage.
            Hot Key : ./c-ptt-g-i
        """
        embed = dc.Embed(
            title = " 🔎🐍 Check ptt gossiping Board Title Information",
            description = "\
                ptt gossiping 看板 標題 爬蟲 使用說明\n\n\
                ./check_ptt_gossiping_information 's Hot Key : ./c-ptt-g-i\n\
                ./check_ptt_gossiping 's Hot Key : ./c-ptt-g-s\n\
                ",
            color = 0xFF5733
        )
        embed.add_field(
            name = "./check_ptt_gossiping(or ./c-ptt-g-s)",
            value = f"爬取 ptt gossiping 的最新一頁的前一頁",
            inline = False
        )
        embed.add_field(
            name = "./check_ptt_gossiping > (or ./c-ptt-g-s >)",
            value = f"爬取 ptt gossiping 的下一頁",
            inline = False
        )
        embed.add_field(
            name = "./check_ptt_gossiping < (or ./c-ptt-g-s <)",
            value = f"爬取 ptt gossiping 的上一頁",
            inline = False
        )
        embed.add_field(
            name = "./check_ptt_gossiping_information(or ./c-ptt-g-i)",
            value = f"查看 __./check_ptt_gossiping__ 功能和如何使用",
            inline = False
        )

        await ctx.send(embed = embed)

    @commands.command(aliases = ["c-ptt-g-s"])
    async def check_ptt_gossiping(self, ctx):
        """
            Crawling ptt gossiping board.
            Hot Key : ./c-ptt-g-s

            爬取 PTT 八卦版 標題。
        """
        """
            Web URL = https://www.ptt.cc/bbs/Gossiping/index.html
            Target = HTML gossip titles
        """

        ptt_titles = [[' ' for i in range(3)] for i in range(20)]

        global ptt_gossip_newest_url
        global ptt_gossip_now_url
        global ptt_gossip_page
        global ptt_gossip_now_page

        # 函式：接收使用者輸入並過濾指令提式與語，傳回字串
        def ptt_gossip_input() -> str:

            if ctx.author == self.bot.user:
                return
            else:
                # 獲取輸入訊息
                get_msg = ctx.message.content
                msg = ""
            
                # 過濾開頭指令提示語
                if ("" + get_msg[0 : 22]) == "./check_ptt_gossiping ":
                    msg = "" + get_msg[18 : len(get_msg)]
                elif ("" + get_msg[0 : 12]) == "./c-ptt-g-s ":
                    msg = "" + get_msg[12 : len(get_msg)]

                return msg

        # 函式：開始爬蟲
        def crawling(cmd : str, url : str) -> str:

            web_request = req.Request(url, headers = 
            {
                "cookie" : "over18=1",
                "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
            })

            with req.urlopen(url = web_request) as response:
                web_data = response.read().decode("utf-8")
            
            web_fitter = bs4.BeautifulSoup(web_data, "html.parser")


            web_titles = web_fitter.find_all("div", class_ = "title")
            
            times = 0
            for target in web_titles:
                if target.a != None:
                    # await ctx.send(target.a.string)
                    ptt_titles[times][0] = str(target.a.string)
                    ptt_titles[times][1] = str(target.a["href"])

                    times += 1
            
            web_date = web_fitter.find_all("div", class_ = "date")
            
            times = 0
            for target in web_date:
                if target != None:
                    ptt_titles[times][2] = str(target.string)

                    times += 1

            if cmd == '>':
            
                pass_url = web_fitter.find("a", string = "下頁 ›")

                return str("https://www.ptt.cc/" + pass_url["href"])
            
            elif cmd == '<':

                pass_url = web_fitter.find("a", string = "‹ 上頁")

                return str("https://www.ptt.cc/" + pass_url["href"])

            return url

        # 函式：製作 Embed
        def make_embed():

            embed = dc.Embed(
                title = " 💬 ptt gossiping Board Title",
                description = "ptt gossiping 看板 標題",
                color = 0xFF5733
            )
            for i in range(20):

                if ptt_titles[i][0] != ' ' and ptt_titles[i][1] != ' ' and ptt_titles[i][2] != ' ':

                    embed.add_field(
                        name = f"{ptt_titles[i][0]}",
                        value = f"\
                            __{ptt_titles[i][1]}__\n\
                            **{ptt_titles[i][2]}**\
                            ",
                        inline = False
                    )

            embed.add_field(
                name = "Page 頁數",
                value = f"page : {ptt_gossip_now_page}",
                inline = False
            )
            
            return embed

        user_input = ptt_gossip_input()
        # print(f"user_input : {user_input}")

        if user_input == "":

            ppt_gossip_now_url = crawling('0', ptt_gossip_newest_url)

            await ctx.send(embed = make_embed())
        
        elif user_input == '>':
            
            ptt_gossip_now_page += 1
            
            if ptt_gossip_now_page == ptt_gossip_page + 1:
                ptt_gossip_now_page = 0
            
            url = "https://www.ptt.cc/bbs/Gossiping/index" + str(ptt_gossip_now_page) + ".html"

            try:

                crawling('0', url)
                # ppt_gossip_now_url = crawling('>', ppt_gossip_now_url) 

                await ctx.send(embed = make_embed())

            except:

                embed = dc.Embed(
                    title = "❌ Sorry : error web url",
                    description = "Please tell the developer this error situation.(the target url must be changed.)",
                    color = 0x7E3D76
                )

                await ctx.send(embed = embed)

        elif user_input == '<':

            if ptt_gossip_now_page == 0:
                ptt_gossip_now_page = ptt_gossip_page + 1

            ptt_gossip_now_page -= 1

            url = "https://www.ptt.cc/bbs/Gossiping/index" + str(ptt_gossip_now_page) + ".html"

            try:

                crawling('0', url)
                # ppt_gossip_now_url = crawling('<', ppt_gossip_now_url)

                await ctx.send(embed = make_embed())

            except:

                embed = dc.Embed(
                    title = "❌ Sorry : error web url",
                    description = "Please tell the developer this error situation.(the target url must be changed.)",
                    color = 0x7E3D76
                )

                await ctx.send(embed = embed)
        
        else:
            
            embed = dc.Embed(
                title = "❌ Sorry : error input",
                description = "Please go to check command information to know how to use.",
                color = 0x7E3D76
            )

            await ctx.send(embed = embed)

    @commands.command(aliases = ["c-d-i"])
    async def detect_earthquake_information(self, ctx):
        """
            Shows ./detect_earthquake 's usage.
            Hot Key : ./c-d-i
        """
        embed = dc.Embed(
            title = " 🔎🐍 Check ptt movie Board Title Information",
            description = "\
                ptt movie 看板 標題 爬蟲 使用說明\n\n\
                ./check_ptt_movie_information 's Hot Key : ./c-ptt-m-i\n\
                ./check_ptt_movie 's Hot Key : ./c-ptt-m-s\n\
                ",
            color = 0xFF5733
        )
        embed.add_field(
            name = "./check_ptt_movie(or ./c-ptt-m-s)",
            value = f"爬取 ptt movie 的最新一頁的前一頁",
            inline = False
        )
        embed.add_field(
            name = "./check_ptt_movie > (or ./c-ptt-m-s >)",
            value = f"爬取 ptt movie 的下一頁",
            inline = False
        )
        embed.add_field(
            name = "./check_ptt_movie < (or ./c-ptt-m-s <)",
            value = f"爬取 ptt movie 的上一頁",
            inline = False
        )
        embed.add_field(
            name = "./check_ptt_movie_information(or ./c-ptt-m-i)",
            value = f"查看 __./check_ptt_movie__ 功能和如何使用",
            inline = False
        )

        await ctx.send(embed = embed)

    @commands.command(aliases = ["c-d-s"])
    async def detect_earthquake(self, ctx):
        """
            Detects CWB currently earthquakes.
            Hot Key : ./c-d-s

            爬取 交通部中央氣象局-最近地震 標題。
        """
        """
            Web URL = https://www.cwb.gov.tw/V8/C/E/index.html
            Document URL = https://www.cwb.gov.tw/V8/C/E/MOD/MAP_LIST.html?T=2022082817-2
            Target = HTML XHR titles
        """

        # 原網站已經排序好了，只要順著便可以
        # far-dot & dot 是分開的 class
        # dot_sorted = [[' ' for i in range(2)] for j in range(CWB_LIMIT)]
        # far_dot_sorted = [[' ' for i in range(2)] for j in range(CWB_LIMIT)]

        # 儲存目標資訊
        CWB_titles = [[' ' for i in range(7)] for j in range(CWB_LIMIT)]
        # print(CWB_titles)
        # CWB_store_count = 0
        CWB_website = "https://www.cwb.gov.tw/V8/C/E/index.html"
        """
            0 : 編號     
            1 : Text(no split)
            2 : 區域
            3 : 時間
            4 : 地點
            5 : 深度
            6 : 地震規模
        """

        def input() -> str:
            if ctx.author == self.bot.user:
                return
            else:
                get_msg = ctx.message.content
                msg = ""
            
                if ("" + get_msg[0 : 20]) == "./detect_earthquake ":
                    msg = "" + get_msg[20 : len(get_msg)]
                elif ("" + get_msg[0 : 8]) == "./c-d-s ":
                    msg = "" + get_msg[8 : len(get_msg)]

                return msg
        
        def crawling() -> None:

            # global CWB_store_count

            web_request = req.Request(CWB_earthquake_file_url, headers = 
            {
                "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"
            })

            with req.urlopen(url = web_request) as response:
                web_data = response.read().decode("utf-8")
            
            web_fitter = bs4.BeautifulSoup(web_data, "html.parser")

            """
                dot, far-dot, dot lg-dot
            """
            web_dot = web_fitter.find_all("a", class_ = "dot")
            web_far_dot = web_fitter.find_all("a", class_ = "far-dot")
            web_lg_dot = web_fitter.find_all("a", class_ = "dot lg-dot")
            # print(web_dot)
            # print(web_far_dot)

            # times = 0
            for target in web_dot:

                data_name = str(target["data-name"])
                number = "" + data_name[3 : ]
                number = int(number)

                CWB_titles[number - 1][0] = str(number)
                CWB_titles[number - 1][1] = str(target.string)

                # times += 1

            # if web_far_dot[0] != "None":
            try:
                for target in web_far_dot:
                    
                    data_name = str(target["data-name"])
                    number = "" + data_name[3 : ]
                    number = int(number)

                    CWB_titles[number - 1][0] = str(number)
                    CWB_titles[number - 1][1] = str(target.text)

            except:
                pass

            try:
                for target in web_lg_dot:
                    
                    data_name = str(target["data-name"])
                    number = "" + data_name[3 : ]
                    number = int(number)

                    CWB_titles[number - 1][0] = str(number)
                    CWB_titles[number - 1][1] = str(target.text)
                    # print(CWB_titles[number - 1][1]) 

                    # times += 1
            except:
                pass
            # print(CWB_titles[1])
            
            # 這個泡沫排序不太對喔，他把我資料打亂了XD，原本排好的說。
            # for i in range(0, 15, 1):
            #     for j in range(0, i, 1):

            #         if CWB_titles[j][0] > CWB_titles[i][0]:
                        
            #             temp = CWB_titles[j][0]
            #             CWB_titles[j][0] = CWB_titles[i][0]
            #             CWB_titles[i][0] = temp

            #             temp = CWB_titles[j][1]
            #             CWB_titles[j][1] = CWB_titles[i][1]
            #             CWB_titles[i][1] = temp

            # print(CWB_titles)

            for i in range(0, CWB_LIMIT, 1):

                words = CWB_titles[i][1].split("，")
                # print(words[0])
                # print(words)

                # words may be 'None'
                # e.g. words[0] == "None"
                if words[0] != "None" and words[0] != " ":
                    
                    CWB_titles[i][2] = words[0]
                    CWB_titles[i][3] = words[1]
                    CWB_titles[i][4] = words[2]
                    CWB_titles[i][5] = words[3]
                    CWB_titles[i][6] = words[4]

                        # for j in range(1, 6, 1):

                        #     CWB_titles[i][j + 1] = words[j - 1]
                #     else:
                        
                #         CWB_store_count = i

                #         return

                # CWB_store_count = 100

            return  

        def make_embed():
            
            # global CWB_store_count

            embed = dc.Embed(
                title = " 🌋 交通部中央氣象局——最近地震 標題",
                description = "CWB Board Title",
                color = 0xFF5733
            )
            for i in range(0, 15, 1):
                
                # if CWB_titles[i][0] != None:

                embed.add_field(
                    name = f"地震時間：{CWB_titles[i][3]}",
                    value = f"\
                        形成地點：{CWB_titles[i][4]}\n\
                        影響區域：{CWB_titles[i][2]}\n\
                        地震規模：**{CWB_titles[i][6]}**\n\
                        地震深度：{CWB_titles[i][5]}\n\
                        地震編號：**{CWB_titles[i][0]}** __{CWB_website}__\n\n\n\
                        ",
                    inline = False
                )
            
            return embed

        # user_input = input()

        crawling()
        # print(CWB_titles)

        await ctx.send(embed = make_embed())


def setup(bot):
    bot.add_cog(Crawler(bot))