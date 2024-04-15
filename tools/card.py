import discord
import pyshorteners
from datetime import datetime


def inf_play(ctx, url=None, title=None, image=None, author=None, like_count=None,foot_msg=None,title_msg=None):
    embed = discord.Embed(title= title_msg, description=title)
    if title:
        if url:
            embed.set_thumbnail(url=image['href'])
            embed.add_field(name="✏️Author ",
                        value=author['content'], inline=True)
            embed.add_field(name="  ", value="   ")
            embed.add_field(name=f"👍Likes", value=like_count, inline=True)
            short_url = pyshorteners.Shortener().tinyurl.short(url)
            embed.add_field(name="Video link", value=short_url)
    avatar_img = (str(ctx.author.avatar)[:-10])
    embed.set_footer(
        text=f"{ctx.author.nick} {foot_msg} {datetime.now().strftime('%H:%M')}", icon_url=avatar_img)
    return embed