#import asyncio
#import yt_dlp
import discord
#import ffmpeg
from tools.card import inf_play
from tools.music_info import music_inf

class playfun():
    async def p_music(self,ctx,msg):
        try:
            title_msg = "Now playing..."
            foot_msg = "order this song."
            embed=inf_play(ctx, url=msg, title=self.music_queue[0]['music_name'], image=self.music_queue[0]['video_title_image'], author=self.music_queue[0]['author'], like_count=self.music_queue[0]['like_count'],foot_msg=foot_msg,title_msg=title_msg)
        except Exception as  e:
            print(e)

        #First song every times
        m_url = self.music_queue[0]['song']
        if self.play_count == 0:
            self.music_queue.pop(0)
            self.play_count += 1

            self.isplaying = True

            player = discord.FFmpegOpusAudio(m_url, **self.ffmpeg_options)
            self.isplaying = True
            self.ispaused = False
            await ctx.send(embed=embed)
            #song = music_inf(self,song['song'])
            self.voice_clients[ctx.guild.id].play(player,after=lambda e: self.play_next(ctx))


    async def n_music(self,ctx):
            print('Run play_next...')
            if len(self.music_queue) > 0:
                self.isplaying = True
                m_url = self.music_queue[0]['song']

                player = discord.FFmpegOpusAudio(m_url, **self.ffmpeg_options)
                try:
                    title_msg = "Now playing..."
                    foot_msg = "order this song."
                    embed=inf_play(ctx, url=self.music_queue[0]['song'],title=self.music_queue[0]['music_name'], image=self.music_queue[0]['video_title_image'], author=self.music_queue[0]['author'], like_count=self.music_queue[0]['like_count'],foot_msg=foot_msg,title_msg=title_msg)
                    await ctx.send(embed=embed)
                except Exception as  e:
                    print(e)
                self.music_queue.pop(0)
                self.isplaying = True
                self.ispaused = False

                #async def callback(e):
                #    self.bot.loop.create_task((await self.play_next(ctx,msg)))
                    
                self.voice_clients[ctx.guild.id].play(player,after=lambda e: self.play_next(ctx))#await self.play_next(ctx,msg))
            else:
                self.isplaying = False
                