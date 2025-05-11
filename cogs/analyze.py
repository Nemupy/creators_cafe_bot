import discord
from discord.ext import commands

class Analyze(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="role_analyze", aliases=["r"])
    @commands.has_permissions(administrator=True)
    async def role_analyze(self, ctx, *roles: discord.Role):
        if not roles:
            roles = ctx.guild.roles
            roles = [role for role in roles if role != ctx.guild.default_role]

        total_members = len(ctx.guild.members) 

        embed = discord.Embed(color=discord.Color.blue())

        for role in roles:
            role_members = len([member for member in ctx.guild.members if role in member.roles])
            percentage = (role_members / total_members) * 100
            progress_bar = self.create_progress_bar(percentage)
            embed.add_field(
                name=f"",
                value=f"{role.mention} {percentage:.2f}% ({role_members}/{total_members})\n{progress_bar}",
                inline=False
            )

        await ctx.send(embed=embed)

    def create_progress_bar(self, percentage, length=20):
        filled_length = int(length * percentage // 100)
        bar = "█" * filled_length + "░" * (length - filled_length)
        return f"`{bar}`"

async def setup(bot):
    await bot.add_cog(Analyze(bot))