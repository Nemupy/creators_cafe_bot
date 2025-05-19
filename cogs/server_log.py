import datetime
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

LOG_CHANNEL_ID = int(os.getenv("LOG_CHANNEL_ID"))

class ServerLog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.log_channel = self.bot.get_channel(LOG_CHANNEL_ID)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        embed = discord.Embed(description=f"{member.mention} がサーバーに参加しました。", color=0x90b4de)
        embed.set_author(name=member.name, icon_url=member.display_avatar.url)
        embed.set_footer(text=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        await self.log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        embed = discord.Embed(description=f"{member.mention} がサーバーから退出しました。", color=0xd9a3cd)
        embed.set_author(name=member.name, icon_url=member.display_avatar.url)
        embed.set_footer(text=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        await self.log_channel.send(embed=embed)

async def setup(bot):
    await bot.add_cog(ServerLog(bot))