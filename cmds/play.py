from discord.ext import commands
from core.maincog import MainCog
import asyncio
import yt_dlp
import discord
import ffmpeg
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from tools.card import inf_play
from tools.connect import conn

class play(MainCog):

    def music_info(self,msg):
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
    def play_next(self,ctx):
        '''await ctx.send(embed=embed)
        try:
            title_msg = "Now playing..."
            foot_msg = "order this song."
            embed=inf_play(ctx, url=msg, title=self.music_queue[0]['music_name'], image=self.music_queue[0]['video_title_image'], author=self.music_queue[0]['author'], like_count=self.music_queue[0]['like_count'],foot_msg=foot_msg,title_msg=title_msg)
        except Exception as  e:
            print(e)'''
        print('Run play_next...')
        if len(self.music_queue) > 0:
            self.isplaying = True
            m_url = self.music_queue[0]['song']

            self.music_queue.pop(0)

            player = discord.FFmpegOpusAudio(m_url, **self.ffmpeg_options)
            self.isplaying = True
            self.ispaused = False

            #async def callback(e):
            #    self.bot.loop.create_task((await self.play_next(ctx,msg)))
                
            self.voice_clients[ctx.guild.id].play(player,after=lambda e: self.play_next(ctx))#await self.play_next(ctx,msg))
        else:
            self.isplaying = False

    async def p_music(self,ctx,msg):
        try:
            title_msg = "Now playing..."
            foot_msg = "order this song."
            embed=inf_play(ctx, url=msg, title=self.music_queue[0]['music_name'], image=self.music_queue[0]['video_title_image'], author=self.music_queue[0]['author'], like_count=self.music_queue[0]['like_count'],foot_msg=foot_msg,title_msg=title_msg)
        except Exception as  e:
            print(e)

        m_url = self.music_queue[0]['song']
        if self.play_count == 0:
            self.music_queue.pop(0)
            self.play_count += 1

        self.isplaying = True

        player = discord.FFmpegOpusAudio(m_url, **self.ffmpeg_options)
        self.isplaying = True
        self.ispaused = False
        await ctx.send(embed=embed)
        #def callback(e):
        #    self.bot.loop.create_task((self.play_next(ctx,msg)))
        self.voice_clients[ctx.guild.id].play(player,after=lambda e: self.play_next(ctx))#await self.play_next(ctx,msg))
                #await ctx.send(embed=embed)
        #else:
        #    self.isplaying = False

    @commands.command(name="Play",description="To play music",aliases=["p"])  # read input
    async def play_music(self, ctx, msg=None):
        #Detect the author in voice channel
        try:
            voice_channel = ctx.author.voice.channel.connect
        except:
            await ctx.send("You need connect voice channel first....")
            return
        
        #connect voice channel
        if self.vc is False:
            self.vc = True
            await conn(ctx,self)
        
        #Chck msg
        if msg:
            #Check msg arguments
            if msg[:5] != "https":
                title_msg = "arguments format wrong..."
                await ctx.send(embed=inf_play(ctx,title_msg=title_msg))
                return
            else:
                song = self.music_info(msg)
                self.music_queue.append(song)
                if self.isplaying == False:
                    await self.p_music(ctx,msg)
                    #await asyncio.gather(self.p_music(ctx,msg))

        #Resume music
        else:
            #If music is stoped
            if self.ispaused and self.isplaying is False:
                self.ispaused = False
                self.isplaying = True
                self.voice_clients[ctx.guild.id].resume()
                title_msg = "Music keep playing..."
                foot_msg = "resume"
                embed = inf_play(ctx,title_msg=title_msg,foot_msg=foot_msg)
                await ctx.send(embed=embed)
            #If music is playing
            else:
                title_msg = "Music is played"
                foot_msg = " "
                embed = inf_play(ctx,title_msg=title_msg,foot_msg=foot_msg)
                await ctx.send(embed=embed)

    @commands.command(name="Pause",description="To pause music",aliases=["pa"])
    async def pause_music(self,ctx):
        #If music is stoped
        if self.isplaying is False:
            title_msg = "No music is playing..."
            embed = inf_play(ctx,title_msg=title_msg)
            await ctx.send(embed=embed)
            return
        #If music is playing
        else:
            self.voice_clients[ctx.guild.id].pause() 
            title_msg = "Music stop"
            button_msg = "stopped"
            embed = inf_play(ctx,title_msg=title_msg,foot_msg=button_msg)
            await ctx.send(embed=embed)
            self.ispaused = True
            self.isplaying = False  
    
    @commands.command(name="Skip",description="Skip music",aliases=["sk"])
    async def skip(self,ctx):
        print('Run skip function...')
        if self.isplaying:
            self.voice_clients[ctx.guild.id].stop()
            #self.play_next(ctx)
            print('skip...')
        else:
            print('Not music is playing...')

    @commands.command(name="list",description="Show music queue",aliases=["li"])
    async def list(self,ctx):  
        if len(self.music_queue) > 0:
            await ctx.send('-----Play list-----')
            for i in range(len(self.music_queue)):
                await ctx.send(f"{i+1}-{self.music_queue[i]['music_name']}")
        else:
            await ctx.send("Not music in queue")
async def setup(bot) -> None:
    await bot.add_cog(play(bot))

