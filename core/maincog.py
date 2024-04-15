import discord
from discord.ext import commands


class MainCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

        self.isplaying = False
        self.ispaused = False

        self.voice_channel = None
        self.voice_clients = {}
        self.music_queue = []     
        self. yt_dl_options = {'format': 'bestaudio/best','before_options': '-reconnect 1 -reconnected_streamed 1  -reconnect_delay_max 5','options': '-vn'}
        self.ffmpeg_options = {'options': '-vn',"before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"}
        #self. yt_dl_options = {"format": "bestaudio/best"}
        #self.ffmpeg_options = {'format':'bestaudio','noplaylist':'True'}
