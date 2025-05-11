import datetime
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

LOG_CHANNEL_ID = int(os.getenv("LOG_CHANNEL_ID"))


class VoiceLog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        log_channel = self.bot.get_channel(LOG_CHANNEL_ID)

        if after.channel and not before.channel:
            embed = discord.Embed(description=f"{member.mention} が <#{after.channel.id}> に参加しました。", color=0x90b4de)
            embed.set_author(name=member.name, icon_url=member.display_avatar.url)
            embed.set_footer(text=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            await log_channel.send(embed=embed)

        elif before.channel and not after.channel:
            embed = discord.Embed(description=f"{member.mention} が <#{before.channel.id}> から退出しました。", color=0xd9a3cd)
            embed.set_author(name=member.name, icon_url=member.display_avatar.url)
            embed.set_footer(text=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            await log_channel.send(embed=embed)


async def setup(bot):
    await bot.add_cog(VoiceLog(bot))
