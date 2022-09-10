import discord
from discord.ext import commands
import os
from Core import Cog_Extension

class Music(Cog_Extension):
        
    @commands.command()
    async def play(self, ctx, url):
        song_exist = os.path.isfile("song.mp3")
        try:
            if song_exist:
                os.remove("song.mp3")
        except PermissionError:
            await ctx.send("Wait for the current playing music to end or use the 'stop' command")
            return

        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)

        if voice is None:
            voiceChannel = discord.utils.get(ctx.guild.voice_channels, name='General')
            await voiceChannel.connect(timeout = 600.0)
            voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        
        os.system(f"yt-dlp --extract-audio --audio-format mp3 --audio-quality 0 {url}")

        for file in os.listdir("./"):
            if file.endswith(".mp3"):
                os.rename(file, "song.mp3")
    
        voice.play(discord.FFmpegPCMAudio(executable = 'ffmpeg.exe', source = "song.mp3"))

    
    @commands.command()
    async def leave(self,ctx):
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        try:
                await voice.disconnect()
        except:
            await ctx.send("The bot is not connected to a voice channel.")


    @commands.command()
    async def pause(self,ctx):
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        try: 
            if voice.is_playing():
                voice.pause()
            else:
                await ctx.send("Currently no audio is playing.")
        except:
            await ctx.send("Bot is not connected to a voice channel.")


    @commands.command()
    async def resume(self,ctx):
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        try:
            if voice.is_paused():
                voice.resume()
            else:
                await ctx.send("The audio is not paused.")
        except:
            await ctx.send("Bot is not connected to a voice channel.")

    @commands.command()
    async def stop(self,ctx):
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        try:
            voice.stop()
        except:
            await ctx.send("Bot is not connected to a voice channel.")
    
def setup(bot):
    bot.add_cog(Music(bot))