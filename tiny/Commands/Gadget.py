"""
    存放一些小工具的程式(跟開發前端比較有關係)
"""
import discord as dc
from discord.ext import commands
from Core import Cog_Extension

import datetime
import time

TODO_LIST_MAX_TABLE = 3
TODO_LIST_MAX_EVENT = 4
TODO_LIST_MAX_EVENT_ITEM = 3

class Gadget(Cog_Extension):
    """
        Global Variable
    """
    # To-do List 全域變數

    global Todo_List
    global Todo_List_store_empty

    # To-do List 的儲存陣列(三圍陣列，結構圖如下)
    # 初始化為 ' '(空白)
    Todo_List = [[[' ' for k in range(TODO_LIST_MAX_EVENT_ITEM)] for i in range(TODO_LIST_MAX_EVENT)] for j in range(TODO_LIST_MAX_TABLE)]
    
    # 判斷 Todo_List 是否為全空狀態
    Todo_List_store_empty = True

    """
        To Do List 結構示意圖 
    Table :                  0                                  1     
Event :     |=================================||=================================|
      0     ||(0, 0, 0)||(0, 0, 1)||(0, 0, 2)||||(1, 0, 0)||(1, 0, 1)||(1, 0, 2)||
            |=================================||=================================|
      1     ||(0, 1, 0)||(0, 1, 1)||(0, 1, 2)||||(1, 1, 0)||(1, 1, 1)||(1, 1, 2)||
            |=================================||=================================|
      2     ||(0, 2, 0)||(0, 2, 1)||(0, 2, 2)||||(1, 2, 0)||(1, 2, 1)||(1, 2, 2)||
            |=================================||=================================|
Event Item :      0          1          2            0          1          2

    """

    """
        Function
    """
    @commands.command(aliases = ["p"])
    async def ping(self, ctx) -> None:
        """
            Shows currently ping value.
            Hot Key : ./p
        """
        ping_value = round(self.bot.latency * 1000)

        embed = dc.Embed(
            title = f"{ping_value} ms",
            description = "Current Ping Value",
            color = 0x7E3D76
        )
        await ctx.send(embed = embed)

    @commands.command(aliases = ["c-i"])
    async def clear_information(self, ctx) -> None:
        """
            Show ./clear 's usage.
            Hot Key : ./c-i
        """

        embed = dc.Embed(
            title = " 🔎 Clear Introduce",
            description = "Clear 指令說明",
            color = 0xFF5733
        )
        embed.add_field(
            name = " 📍 範例輸入：",
            value = "\
                **./clear all**\n\
                指令用途：清除全部歷史紀錄\n\
                \n\
                **./clear <number : int>\n\
                指令用途：清除指定數量的歷史紀錄\n\
                ",
            inline = False
        ) 

        await ctx.send(embed = embed)

    @commands.command(aliases = ["c-s"])
    async def clear(self, ctx) -> None:
        """
            Clear chat history.
            Hot Key : c-s

            清除歷史紀錄。
        """
        if ctx.author == self.bot.user:
            return
        
        get_msg = ctx.message.content
        msg = "" + get_msg[8 : len(get_msg)]
        
        embed = dc.Embed(
            description = f"Has been cleared {msg} successfully.",
            color = 0x7E3D76
        )
        await ctx.send(embed = embed)
        
        time.sleep(0.5)

        if msg == "all":
            await ctx.channel.purge()
        else:
            await ctx.channel.purge(limit = int(msg))
        
    @commands.command(aliases = ["todo-i"])
    async def todo_list_introduce(self, ctx):
        """
            Shows ./todo_list 's usage.
            Hot Key : ./todo-i
        """
        def make_Todo_Menu():
            Todo_Menu = dc.Embed(
                title = " 📃 To-do List Introduce",
                description = "To-do List 指令說明\n\n\
                    __./todo_list_introduce__ 's Hot Key : todo-i\n\
                    __./todo_list__ 's Hot Key : todo-s\n\
                    ",
                color = 0xFF5733
            )
            Todo_Menu.add_field(
                name = " 📍 函式參數(Parameter)解釋",
                value = "\
                    <mode> : str —> 輸入你想起用的模式\n\
                    <name> : str —> 輸入你想起用的名稱\n\
                    <number> : int —> 輸入你想加入的工作表(Table)編號\n\
                    <event> : int —> 輸入你想加入工作表裡欄位(Event)編號\n\
                    <item> : int —> 輸入你想加入的工作表裡欄位裡面項目(Event Item)的編號\n\
                    <content> : str —> 輸入你想加入項目中的內容\n\
                    ",
                inline = False
            )
            Todo_Menu.add_field(
                name = "./todo-s add <number : int> <event : int> <item : str> <content : str>",
                value = "指令用途：將內容加入工作表的項目中__...__",
                inline = False
            )
            Todo_Menu.add_field(
                name = "./todo-s create <number : int> <name : str>",
                value = "指令用途：新增工作表__...__",
                inline = False
            )
            Todo_Menu.add_field(
                name = "./todo-s remove <number : int> <event : int> <item : str>",
                value = "指令用途：移除工作表的項目中的內容__...__",
                inline = False
            )
            Todo_Menu.add_field(
                name = "./todo-s empty <number : int>",
                value = "指令用途：清空項目工作表__...__",
                inline = False
            )
            Todo_Menu.add_field(
                name = "./todo-s list <mode : str>",
                value = "指令用途：列出工作表項目暨內容__...__",
                inline = False
            )
            Todo_Menu.add_field(
                name = "./todo-s finish",
                value = "指令用途：結束當前動作__...__",
                inline = False
            )
            Todo_Menu.add_field(
                name = "\
                     📍 想詳閱更多使用資訊\n\
                    請依照需求在呼叫 __./todo_list_introduce__ 後 + 空格 + 數字\n\
                    ",
                value = "\
                    範例輸入：\n\
                    Example Input : ./todo_list_introduce 0\n\
                    \n\
                    # 指令需求編號：\n\
                    (a)add : 0\n\
                    (c)create : 1\n\
                    (r)remove : 2\n\
                    (e)empty : 3\n\
                    (l)list : 4\n\
                    (f)finish : 5\n\
                    \n\
                    # 更多幫助編號：\n\
                    與開發人員聯絡 : -1\n\
                    To-Do List 範例樣式：-2\n\
                    ",
                inline = False
            )
            
            return Todo_Menu

        def make_add_Menu():
            add_Menu = dc.Embed(
                title = " ✨ To-do List Command __add__ Introduce",
                description = "To-do List __add__ 指令說明",
                color = 0xFF5733
            )
            add_Menu.add_field(
                name = "./todo-s add <number : int> <event : int> <item : str> <content : str>",
                value = "\
                 📍 指令用途：將內容加入工作表的項目中。\n\
                細項(Event Item)分別有(編號)：Event(1)、Time(2)、Status(3)\n\
                \n\
                 📍 指令使用前提：\n\
                (1) 儲存格由 1 開始\n\
                (2) 所有輸入的引數中間需空格(尾巴不需再空格)\n\
                (3) 需知道儲存格位置\n\
                (4) 欲加入的工作表需先被創建，否則不得執行\n\
                \n\
                 📍 細項名稱和編號：\n\
                Event：1\n\
                Time：2\n\
                Status：3\n\
                \n\
                 📍 輸入範例：\n\
                Example Input : ./todo-s add 1 1 1 go jogging with yuri.\n\
                輸入意義：\n\
                將內容\"go jogging with yuri.\" 存入Table(工作表) 1 號裡的Event(欄位) 1 號裡的Event Item(項目) 1 號Event(事件)中\n\
                ",
                inline = False
            )

            return add_Menu

        def make_Develope_Menu():
            Develope_Menu = dc.Embed(
                title = "\"fat cat\" Discord Robot Developer",
                url = "https://discord.com/api/oauth2/authorize?client_id=988002605068353587&permissions=534727096384&scope=bot",
                description = "開發 \"fat cat\" Discord Robot 的人員",
                color = 0xfcd7d6, 
                timestamp = datetime.datetime.now()
            )
            Develope_Menu.set_author(
                name = "zong zong",
                url = "https://github.com/zongzong0408",
                icon_url = "https://i.pinimg.com/originals/43/f0/5b/43f05bff9062461590bef9043ba77929.jpg"
            )
            Develope_Menu.set_thumbnail(
                url = "https://i.pinimg.com/originals/67/29/fc/6729fc2f0f62c0ea5784ee66c9595a2f.jpg"
            )
            Develope_Menu.add_field(
                name = "**IG**",
                value = "chu__0408\_",
                inline = True
            )
            Develope_Menu.add_field(
                name = "**Email**",
                value = "zongzongchu0408@gmail.com",
                inline = False
            )
            Develope_Menu.set_footer(text = "Date : 2022/07/03")

            return Develope_Menu

        def make_Default_Menu():

            Default_Menu = dc.Embed(
                title = "This command is no more detail...🐱‍👤",
                description = "這個指令沒有更多的詳細內容了...",
                color = 0xFF5733
            )

            return Default_Menu
        
        def make_Todo_Example():
            """
                e.g. of to-do list：

                Table Name ： 8/13 Morning

                Event ： Go to hiking.
                Time ： 7:00 A.M
                Status ： finished
                
                Event ： Walk the dog.
                Time ： 9:00 A.M
                Status ： not yet

            """
            Todo_Ex = dc.Embed(
                title = "Table name : 8/13 Morning",
                color = 0xFF5733
            )
            Todo_Ex.add_field(
                name = f"Event : Go to hiking.",
                value = f"\
                    Time : **7:00 A.M**\n\
                    Status : **finished**\n\
                    ",
                inline = False
            )
            Todo_Ex.add_field(
                name = f"Event : Walk the dog.",
                value = f"\
                    Time : **9:00 A.M**\n\
                    Status : **not yet**\n\
                    ",
                inline = False
            )

            return Todo_Ex

        # 函式：接收使用者輸入並過濾指令提式與語，傳回字串
        def todo_input() -> str:

            if ctx.author == self.bot.user:
                return
            else:
                # 獲取輸入訊息
                get_msg = ctx.message.content
                msg = ""
            
                # 過濾開頭指令提示語
                if ("" + get_msg[0 : 22]) == "./todo_list_introduce ":
                    msg = "" + get_msg[22 : len(get_msg)]
                elif ("" + get_msg[0 : 9]) == "./todo-i ":
                    msg = "" + get_msg[9 : len(get_msg)]

                return msg
        
        user_input = todo_input()
        
        # 使用者沒有選擇模式，輸出主選單
        if user_input == "":
            
            await ctx.send(embed = make_Todo_Menu())
        
        # 使用者有選擇模式，輸出子選單
        else:
            mode = int(user_input)
            
            if mode == 0:
                
                await ctx.send(embed = make_add_Menu())

            elif mode == -1:

                await ctx.send(embed = make_Develope_Menu())

            elif mode == -2:

                await ctx.send(embed = make_Todo_Example())
            
            else:

                await ctx.send(embed = make_Default_Menu())

    @commands.command(aliases = ["todo-s"])
    async def todo_list(self, ctx):
        """
            The todo list function on discord.
            Hot Key : todo-s
        """
        global Todo_List
        global Todo_List_store_empty

        # 同步函式：判斷 Todo_List 是否為全空狀態
        def judge_Todo_List_is_empty() -> bool:

            for i in range(TODO_LIST_MAX_TABLE):
                for j in range(0, TODO_LIST_MAX_EVENT):
                    for k in range(TODO_LIST_MAX_EVENT_ITEM):
                        
                        if Todo_List[i][j][k] != '':
                            
                            return False

            return True

        # 異步函式：顯示 工作表(Table)
        async def show_list(cmd : str) -> None:
            
            Todo_List_store_empty = judge_Todo_List_is_empty()

            if Todo_List_store_empty == True:

                await ctx.send("All store cell are empty. pls create a new Table.")
                return 

            # 輸出全部的 Table
            if cmd == "all":

                for table in range(0, TODO_LIST_MAX_TABLE, 1):
                    
                    if Todo_List[table][0][0] != ' ':
                        # 製作不同工作表的 Embed
                        todo_list_embed = dc.Embed(
                            title = f"Table name : {Todo_List[table][0][0]}",
                            color = 0xFF5733
                        )

                        for event in range(1, TODO_LIST_MAX_EVENT, 1):
                            # 加入事件進入 Embed
                            todo_list_embed.add_field(
                                name = f"Event : {Todo_List[table][event][0]}",
                                value = f"\
                                    Time : **{Todo_List[table][event][1]}**\n\
                                    Status : **{Todo_List[table][event][2]}**\n\
                                    ",
                                inline = False
                            )

                        await ctx.send(embed = todo_list_embed)
            
            # 不輸出完全空白的 Table，有存資料就會輸出
            elif cmd == "abridge":
                
                empty_store = 0

                for table in range(TODO_LIST_MAX_TABLE):
                    for event in range(1, TODO_LIST_MAX_EVENT, 1):
                        for item in range(TODO_LIST_MAX_EVENT_ITEM):
                            if Todo_List[table][event][item] == ' ':
                                empty_store += 1

                    # 計算若全空的格子有幾個，再做判斷
                    if empty_store == (TODO_LIST_MAX_EVENT - 1) * TODO_LIST_MAX_EVENT_ITEM:
                        
                        continue

                    else:

                        todo_list_embed = dc.Embed(
                            title = f"Table name : {Todo_List[table][0][0]}",
                            color = 0x2894FF
                        )

                        for event in range(1, TODO_LIST_MAX_EVENT, 1):
                            todo_list_embed.add_field(
                                name = f"Event : {Todo_List[table][event][0]}",
                                value = f"\
                                    Time : **{Todo_List[table][event][1]}**\n\
                                    Status : **{Todo_List[table][event][2]}**\n\
                                    ",
                                inline = False
                            )

                        await ctx.send(embed = todo_list_embed)

            # 只輸出完整的 Table
            elif cmd == "full":

                empty_store = 0

                for table in range(TODO_LIST_MAX_TABLE):
                    for event in range(1, TODO_LIST_MAX_EVENT, 1):
                        for item in range(TODO_LIST_MAX_EVENT_ITEM):
                            if Todo_List[table][event][item] == ' ':
                                empty_store += 1
                
                    if empty_store == (TODO_LIST_MAX_EVENT - 1) * TODO_LIST_MAX_EVENT_ITEM:
                        
                        todo_list_embed = dc.Embed(
                            title = f"Table name : {Todo_List[table][0][0]}",
                            color = 0x2894FF
                        )

                        for event in range(1, TODO_LIST_MAX_EVENT, 1):
                            todo_list_embed.add_field(
                                name = f"Event : {Todo_List[table][event][0]}",
                                value = f"\
                                    Time : **{Todo_List[table][event][1]}**\n\
                                    Status : **{Todo_List[table][event][2]}**\n\
                                    ",
                                inline = False
                            )

                        await ctx.send(embed = todo_list_embed)
            
            elif cmd.isdigit() == True:
                
                table = int(cmd)

                todo_list_embed = dc.Embed(
                    title = f"Table name : {Todo_List[table][0][0]}",
                    color = 0x2894FF
                )

                for event in range(1, TODO_LIST_MAX_EVENT, 1):
                    todo_list_embed.add_field(
                        name = f"Event : {Todo_List[table][event][0]}",
                        value = f"\
                            Time : **{Todo_List[table][event][1]}**\n\
                            Status : **{Todo_List[table][event][2]}**\n\
                            ",
                        inline = False
                    )
                        

                await ctx.send(embed = todo_list_embed)

            return

        # 同步函式：紀錄使用者輸入
        def todo_input() -> str:
            
            if ctx.author == self.bot.user:
                return 0    
            else:
                # 獲取輸入訊息
                get_msg = ctx.message.content
            
                # 過濾開頭指令提示語
                if ("" + get_msg[0 : 12]) == "./todo_list ":
                    mode_msg = "" + get_msg[12 : len(get_msg)]
                elif ("" + get_msg[0 : 9]) == "./todo-s ":
                    mode_msg = "" + get_msg[9 : len(get_msg)]
                # print(mode_msg)

                return mode_msg

        """
            
        """
        # 程式啟動提醒
        # await ctx.send("<The to-do list program is running.>")
        
        Todo_List_store_empty = judge_Todo_List_is_empty()

        # e.g. msg = "add 1 1 1 halo!"
        msg = todo_input()

        message = []
        message = (msg).split(" ")

        # 模式選擇
        command = message[0]

        if command == "add" or command == 'a':
            """
                ./todo-s add <number : int> <event : int> <item : str> <content : str>
                <number>    :   想加入事件的 工作表(Table)      編號 
                <event>     :   想加入事件的 欄位(Event)        編號
                <item>      :   想加入事件的 項目(Event Item)   名稱
                <content>   :   想加入事件的 訊息               內容
            """

            number = int(message[1]) - 1
            event = int(message[2])
            item = int(message[3]) - 1
            content = ""

            # 過濾 msg 提取純內容(content)
            if command == "add":
                content = "" + msg[10 : ]
            elif command == 'a':
                content = "" + msg[8 : ]

            if Todo_List[number][0][0] != ' ':

                if Todo_List[number][event][item] == ' ':

                    try:
                    
                        Todo_List[number][event][item] = content
                    
                        await show_list(cmd = "all")
                    
                    except:
                        
                        await ctx.send("Table index out of range.")
                        await ctx.send("Please use command __list__ see store situation.")

                else:

                    await ctx.send("Table storage full, please change table to store.")

            else:

                await ctx.send("Please create a table before add new event.")

        elif command == "create" or command == 'c':
            """
                ./todo-s create <number : int> <name : str>
                <number>    :   創造的 工作表 編號 
                <name>      :   創造的 工作表 名稱
            """      
            number = int(message[1]) - 1

            if command == "create":
                name = "" + msg[9 : ]
            elif command == 'c':
                name = "" + msg[4 : ]
            
            if Todo_List[number][0][0] != ' ':

                await ctx.send("The Table is already bing established.")

            else:

                Todo_List[number][0][0] = name

                await show_list(cmd = "all")

        elif command == "remove" or command == 'r':
            """
                ./todo-s remove <number : int> <event : int> <item : str>
                <number>    :   想刪除事件的 工作表 編號 
                <event>     :   想刪除事件的 欄位   編號
                <item>      :   想刪除事件的 項目   名稱
            """
            number = int(message[1]) - 1
            event = int(message[2])
            item = int(message[3]) - 1

            Todo_List[number][event][item] = ' '

            await show_list(cmd = "all")

        elif command == "empty" or command == 'e':
            """
                ./todo-s clear <number : int>
                <number>    :   想刪除事件的 工作表 編號 
            """
            number = int(message[1]) - 1

            for i in range(1, TODO_LIST_MAX_EVENT, 1):
                for j in range(0, TODO_LIST_MAX_EVENT_ITEM, 1):
                    Todo_List[number][i][j] = ' '

            await show_list(cmd = "all")

        elif command == "list" or command == 'l':
            """
                ./todo-s list <mode : str>
                <mode> : 選取模式
                    |- all      :   顯示全部的 Table 表的全部資訊(包括 Event 欄位、Event Item 事項)
                    |- abridge  :   顯示有存資料的 Table 表的全部資訊
                    |- full     :   顯示全滿的 Table 表的全部資訊
                    |- <int>    :   顯示某個 Table 表的全部資訊
            """
            mode = ""
            
            if command == "list":
                mode = "" + msg[5 : ]
            elif command == 'l':
                mode == "" + msg[2 : ]
            
            if mode == "all" or mode == None:

                await show_list(cmd = "all")
            
            if mode == "abridge":

                await show_list(cmd = "abridge")
            
            elif mode == "full":

                await show_list(cmd = "full")

            elif mode.isdigit() == True:

                await show_list(mode)

        elif command == "finish" or command == 'f':
            """
                ./todo-s Exit
            """

            return

def setup(bot):
    bot.add_cog(Gadget(bot))