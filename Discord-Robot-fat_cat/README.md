# _**Developer's Diary**_    

- ## **重要宣告 _Proclaim_**  
    > Using **Python 3.7.0**  
    > Remember install requirements.txt  

    ```python
    pip install requirements.txt
    ```

    在本地執行時若載入模組有誤，可以看是否是模組需加入 .vscode 資料夾

- ## **日期紀錄 _Date_**  
    `2022/07/08 :`  
    > 完成完整的 Discord 輸入流程撰寫。  

    > 局部範例程式碼：
    ```python
    """
    其實不一定需要在參數(Parameter)中裏添加 msg 當作存放 Discord 輸入的值，
    ctx 屬性裏面就已經有包含了。
    """
    # 範例輸入如下
    @commands.command()
    async def test_input(self, ctx):
        # ctx 包含的內容
        print(f"ctx : {ctx}")
        # ctx.message.content 包含的內容
        print(f"ctx.message.content : {ctx.message.content}")
        # 取出完整的 input 內容，(去除指令名稱 <test_input> + 一個空格即可)
        get_msg = ctx.message.content
        msg = "" + get_msg[11 : len(get_msg)]
        print(msg)

    # 多餘的撰寫方式
    async def test_input(self, ctx, msg):
    ```
    `2022/09/09 :`
    > 讓 Discord Robot 24/7 在線上。  
    > 使用 Replit 線上 IDE

    ```python
    """
    他的 Python 版本 3.8.12 會讓我的 bot 出錯(但是可以執行)
    成功執行並上線，但是不會回應任何指令
    (我覺得是我撰寫 bot 的架構不被新版本支援，倘若 bot 指令集中在 Bot.py 應該可以?)
    """
    ```
