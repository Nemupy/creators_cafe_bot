import discord
from discord.ext import commands


class Analyze(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.role_ids = [
            1356118296768020511,
            1356118343974649973,
            1356116939600166983,
            1356120364488458392,
            1356118179033645106,
            1358087693879345182,
            1358087693879345182,
            1356118433095487591,
            1356641761388265552
        ]
        self.gender_ids = [
            1356117038447464629,
            1356116995531083868
        ]

    @commands.command(name="role_analyze", aliases=["r"])
    @commands.has_permissions(administrator=True)
    async def role_analyze(self, ctx, *args):
        if not args:
            roles = [role for role in ctx.guild.roles if role != ctx.guild.default_role]
        elif len(args) == 1 and args[0].lower() == "roles":
            roles = [role for role in ctx.guild.roles if role.id in self.role_ids]
        elif len(args) == 1 and args[0].lower() == "gender":
            roles = [role for role in ctx.guild.roles if role.id in self.gender_ids]
        else:
            roles = []
            for arg in args:
                role = discord.utils.get(ctx.guild.roles, mention=arg)
                if not role:
                    role = discord.utils.get(ctx.guild.roles, name=arg)
                if not role:
                    try:
                        role = await commands.RoleConverter().convert(ctx, arg)
                    except commands.BadArgument:
                        continue
                if role:
                    roles.append(role)

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
