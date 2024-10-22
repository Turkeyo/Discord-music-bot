from discord.ext import commands
from core.maincog import MainCog
from tools.card import inf_play
from tools.connect import connect
from tools.playmusic import playfun
from tools.music_info import music_inf

class play(MainCog):

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
            await connect.conn(ctx,self)
        
        #Chck msg
        if msg:
            #Check msg arguments
            if msg[:5] != "https":
                title_msg = "arguments format wrong..."
                await ctx.send(embed=inf_play(ctx,title_msg=title_msg))
                return
            else:
                song = music_inf(self,msg)
                self.music_queue.append(song)
                if self.isplaying == False:
                    print('run p_music fun')
                    await playfun.p_music(self,ctx,msg)

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
            elif self.isplaying and self.ispaused is False:
                title_msg = "Music is played"
                foot_msg = " "
                embed = inf_play(ctx,title_msg=title_msg,foot_msg=foot_msg)
                await ctx.send(embed=embed)
            #If music is not playing
            elif self.isplaying is False and self.ispaused is False:
                title_msg = "No music playing"
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
        if self.isplaying is True:
            self.voice_clients[ctx.guild.id].stop()
            title_msg = "Skip music..."
            embed = inf_play(ctx,title_msg=title_msg)
            await ctx.send(embed=embed)
            #await playfun.n_music(self,ctx)
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

    @commands.command(name="Disconnect",description="Disconnect voice channel",aliases=["di"])
    async def disconnect(self,ctx):
        await connect.dis_conn(ctx,self)
        self.isplaying = False
        self.ispaused = False
        self.music_queue = []
        self.voice_clients = {}
        self.vc = False
        self.play_count = 0
        self.voice_channel = None

async def setup(bot) -> None:
    await bot.add_cog(play(bot))

