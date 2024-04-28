import asyncio
async def conn(ctx,self):
    print('First to connect the channel')
    #connect the channel (We will see the bot in the voice channel)
    self.voice_channel = await ctx.author.voice.channel.connect()
    self.voice_clients[self.voice_channel.guild.id] = self.voice_channel