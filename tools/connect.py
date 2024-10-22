import asyncio
class connect():
    async def conn(ctx,self):
        print('First to connect the channel')
        #connect the channel (We will see the bot in the voice channel)
        try:
            self.voice_channel = await ctx.author.voice.channel.connect()
            self.voice_clients[self.voice_channel.guild.id] = self.voice_channel
        except Exception as e:
            print(e)

    async def dis_conn(ctx,self):
        print('Disconnect the channel')
        #connect the channel (We will see the bot in the voice channel)
        await self.voice_clients[ctx.guild.id].disconnect()