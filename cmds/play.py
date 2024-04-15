from discord.ext import commands
from core.maincog import MainCog
import asyncio
import yt_dlp
import discord
import ffmpeg
import requests
import pyshorteners
from bs4 import BeautifulSoup
from datetime import datetime
from tools.card import inf_play

class play(MainCog): 
    @commands.command(name="Play",description="To play music",aliases=["p"])  # read input
    async def play_music(self, ctx, msg=None):
        if msg:
            if msg[:5] != "https":
                title_msg = "URL fail...."
                await ctx.send(embed=inf_play(ctx,title_msg=title_msg))
                return
            else:
                self.isplaying = True
                self.ispaused = False
                #If the queue has songs
                if len(self.music_queue) > 0:
                    #Get the queue song
                    m_url = self.music_queue.pop(0)
                #If bot in the channel
                else:
                    m_url = msg
                if self.voice_channel is None:
                    print('First to connect the channel')
                    #connect the channel (We will see the bot in the voice channel)
                    self.voice_channel = await ctx.author.voice.channel.connect()
                try:
                    #Set the options
                    ytdl = yt_dlp.YoutubeDL(self.yt_dl_options)
                    #Get channel Id and the object
                    self.voice_clients[self.voice_channel.guild.id] = self.voice_channel
                    info_dict = ytdl.extract_info(m_url,download=False)
                    song = info_dict['url']
                    player = discord.FFmpegOpusAudio(song, **self.ffmpeg_options)
                    self.voice_clients[ctx.guild.id].play(player)

                    #Video information card
                    source = requests.get(m_url).text
                    soup = BeautifulSoup(source, 'html.parser')
                    video_title_image = soup.find('div').find(
                        'link', itemprop="thumbnailUrl")
                    author = soup.find('div').find(
                        'span').find('link', itemprop="name")
                    title_msg = "Now playing..."
                    foot_msg = "order this song."
                    embed=inf_play(ctx, url=m_url, title=info_dict.get('title', None), image=video_title_image, author=author, like_count=info_dict.get('like_count', None),foot_msg=foot_msg,title_msg=title_msg)
                    await ctx.send(embed=embed)
                except Exception as  e:
                    print(e)
        else:
            if self.ispaused is True:
                self.ispaused = False
                self.isplaying = True
                self.voice_clients[ctx.guild.id].resume()
                title_msg = "Music keep playing..."
                foot_msg = "resume"
                embed = inf_play(ctx,title_msg=title_msg,foot_msg=foot_msg)
                await ctx.send(embed=embed)
            else:
                title_msg = "Music is played"
                foot_msg = " "
                embed = inf_play(ctx,title_msg=title_msg,foot_msg=foot_msg)
                await ctx.send(embed=embed)

    @commands.command(name="Pause",description="To pause music",aliases=["pa"])
    async def pause_music(self,ctx):
        if self.isplaying is False:
            title_msg = "No music is playing..."
            embed = inf_play(ctx,title_msg=title_msg)
            await ctx.send(embed=embed)
        else:
            try:
                self.voice_clients[ctx.guild.id].pause()  
                self.ispaused = True
                self.isplaying = False   
                title_msg = "Music stop"
                button_msg = "stopped"
                embed = inf_play(ctx,title_msg=title_msg,foot_msg=button_msg)
                await ctx.send(embed=embed)
            except Exception as e:
                print(e)
    
async def setup(bot) -> None:
    await bot.add_cog(play(bot))
