from tools.card import inf_play
class connect():
    async def conn(ctx,self):
        print('First to connect the channel')
        #connect the channel (We will see the bot in the voice channel)
        self.voice_channel = await ctx.author.voice.channel.connect()
        self.voice_clients[self.voice_channel.guild.id] = self.voice_channel

    async def dis_conn(ctx,self):
        print('Disconnect the channel')
        #connect the channel (We will see the bot in the voice channel)
        await self.voice_clients[ctx.guild.id].disconnect()
        title_msg = "Leave voice channel..."
        await ctx.send(embed=inf_play(ctx,title_msg=title_msg))
        