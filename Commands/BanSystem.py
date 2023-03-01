import discord
from discord.ext import commands
from discord import app_commands

class Ban(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot


    @app_commands.commands.command(name="ban", description="Bans a user from the server")
    @app_commands.describe(user="The user to ban")
    async def ban(self, interaction: discord.Interaction, user: discord.User, reason: str = None):
        if reason is None:
            reason = "No reason provided"

        if user.bot:
            return

        emb = discord.Embed(
            title=f"Ban System",
            description=f"The moderator {interaction.user.mention} has Ban the user {user.mention}",
            color=discord.Colour.red(),
        ).add_field(
            name="Reason",
            value=f"{reason}",
        ).add_field(
            name="Duration",
            value=f"Perma",
        )
        await interaction.response.send_message(embed=emb)
        # await user.ban(reason=f"Banned by {interaction.user}")



async def setup(bot: commands.Bot):
    await bot.add_cog(Ban(bot))
