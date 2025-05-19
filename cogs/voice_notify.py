import asyncio
import datetime
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

NOTIFY_CHANNEL = int(os.getenv("NOTIFY_CHANNEL_ID"))
NOTIFY_ROLE = int(os.getenv("NOTIFY_ROLE_ID"))

class VoiceNotify(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.active_calls = {}

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if member.bot:
            return

        notify_channel = self.bot.get_channel(NOTIFY_CHANNEL)

        if after.channel and not before.channel:
            members = [m for m in after.channel.members if not m.bot]
            if len(members) == 1 and after.channel.id not in self.active_calls:
                async def timer(channel_id, member):
                    await asyncio.sleep(10)
                    channel = self.bot.get_channel(channel_id)
                    if channel and channel_id in self.active_calls:
                        now_members = [m for m in channel.members if not m.bot]
                        if len(now_members) > 0:
                            embed = discord.Embed(title="通話開始", color=0x90b4de)
                            embed.add_field(name="`チャンネル`", value=f"<#{channel_id}>", inline=True)
                            embed.add_field(name="`始めた人`", value=member.mention, inline=True)
                            embed.add_field(name="`開始時間`", value=f"<t:{int(datetime.datetime.now().timestamp())}:f>", inline=True)
                            embed.set_thumbnail(url=member.avatar.url)
                            await notify_channel.send(f"<@&{NOTIFY_ROLE}>", embed=embed)
                            self.active_calls[channel_id]["notified"] = True
                task = asyncio.create_task(timer(after.channel.id, member))
                self.active_calls[after.channel.id] = {
                    "task": task,
                    "start": datetime.datetime.now(),
                    "notified": False,
                    "member": member
                }

        elif before.channel and not after.channel:
            members = [m for m in before.channel.members if not m.bot]
            if before.channel.id in self.active_calls:
                call = self.active_calls[before.channel.id]
                if len(members) == 0 and not call["notified"]:
                    call["task"].cancel()
                    del self.active_calls[before.channel.id]
                    return
                if len(members) == 0 and call["notified"]:
                    start_time = call["start"]
                    end_time = datetime.datetime.now()
                    duration = end_time - start_time
                    duration_str = "{:02}:{:02}:{:02}".format(
                        int(duration.total_seconds() // 3600),
                        int(duration.total_seconds() // 60 % 60),
                        int(duration.total_seconds() % 60)
                    )
                    embed = discord.Embed(title="通話終了", color=0xd9a3cd)
                    embed.add_field(name="`チャンネル`", value=f"<#{before.channel.id}>", inline=True)
                    embed.add_field(name="`通話時間`", value=duration_str, inline=True)
                    await notify_channel.send(embed=embed)
                    del self.active_calls[before.channel.id]

async def setup(bot):
    await bot.add_cog(VoiceNotify(bot))
