from discord.ext import commands
from core.maincog import MainCog
import asyncio
import yt_dlp
import discord
import ffmpeg
import requests
from bs4 import BeautifulSoup
from datetime import datetime

def music_inf(self,msg):
        #Set the options
        ytdl = yt_dlp.YoutubeDL(self.yt_dl_options)
        #Get channel Id and the object
        info_dict = ytdl.extract_info(msg,download=False)
        song = info_dict['url']
        source = requests.get(msg).text
        soup = BeautifulSoup(source, 'html.parser')
        video_title_image = soup.find('div').find('link', itemprop="thumbnailUrl")
        author = soup.find('div').find('span').find('link', itemprop="name")
        like_count = info_dict.get('like_count', None)
        return {"video_title_image":video_title_image,"author":author,"music_name":info_dict.get('title', None),"like_count":like_count,"song":song}