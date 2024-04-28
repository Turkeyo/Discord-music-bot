from discord.ext import commands
from discord.ext.commands.core import command
from core.maincog import MainCog

class Load(MainCog):
    @commands.command()
    async def load(self,ctx,extension):
        try:
            await self.bot.load_extension(f'cmds.{extension}')
            await ctx.send(f'Loaded {extension} done.')
        except extension as e:
            print(e)
    @commands.command()
    async def reload(self,ctx,extension):
        try:
            await self.bot.reload_extension(f'cmds.{extension}')
            await ctx.send(f'Reloaded {extension} done.')
        except extension as e:
            print(e)
    @commands.command()
    async def unload(self,ctx,extension):
        try:
            await self.bot.unload_extension(f'cmds.{extension}')
            await ctx.send(f'Unloaded {extension} done.')
        except extension as e:
            print(e)
            
async def setup(bot):
    await bot.add_cog(Load(bot))