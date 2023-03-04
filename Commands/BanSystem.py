import discord, sqlite3, enum, datetime
from discord.ext import commands
from discord import app_commands

db = sqlite3.connect('db.db')

class Ban(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot


    @app_commands.commands.command(name="ban", description="Bans a user from the server")
    @app_commands.describe(user="The user to ban")
    async def ban(self, interaction: discord.Interaction, user: discord.Member, reason: str = ""):
        if interaction.user.guild_permissions.ban_members:
            if reason == "":
                reason = "No reason provided"

            if user.bot:
                return

            emb = discord.Embed(
                title=f"Ban System",
                description=f"The moderator {interaction.user.mention} has Ban the user {user.mention}",
                color=discord.Colour.red(),
            ).add_field(name="Reason", value=f"{reason}",
            ).add_field(name="Duration", value=f"Perma",)

            emb1 = discord.Embed(
                title=f"Ban System",
                description=f"The moderator {interaction.user.mention} has Ban you",
                color=discord.Colour.red(),
            ).add_field(name="Reason", value=f"{reason}",
            ).add_field(name="Duration", value=f"permanent",)
            
            emb2 = discord.Embed(
                title=f"Ban System",
                description=f"<:Failed:1080584797572833382> You don't have permission to ban any user {user.mention}",
                color=discord.Colour.red(),
            )

            if interaction.user.top_role <= user.top_role:
                await interaction.response.send_message(embed=emb2)
            else:
                await interaction.response.send_message(embed=emb)
                await user.send(embed=emb1)
                await user.ban(reason=f"Banned by {interaction.user}")

        else:
            emb3 = discord.Embed(
                title=f"Ban System",
                description=f"<:Failed:1080584797572833382> You don't have permission to ban any user any user",
                color=discord.Colour.red(),
            )
            await interaction.response.send_message(embed=emb3)


    class Fruits(enum.Enum):
        minuts = 1
        hour = 2
        days = 3


    @app_commands.commands.command(name="tempban", description="Bans a user temporal from the server")
    @app_commands.describe(user="The user to ban")
    async def temp_ban(self, interaction: discord.Interaction, user: discord.Member, time_type: Fruits, time: int, reason: str = ""):
        if interaction.user.guild_permissions.ban_members:
            if reason == "":
                reason = "No reason provided"

            now = int(datetime.datetime.utcnow().timestamp())
            if time_type == self.Fruits.minuts:
                end_time = now + (time * 60)
            elif time_type == self.Fruits.hour:
                end_time = now + (time * 3600)
            elif time_type == self.Fruits.days:
                end_time = now + (time * 86400)


            emb = discord.Embed(
                title=f"Ban System",
                description=f"<:Done:1080584760616820766> The moderator {interaction.user.mention} has Ban the user {user.mention}",
                color=discord.Colour.green(),
            ).add_field(name="Reason", value=f"{reason}",
            ).add_field(name="Duration", value=f"Perma",)

            emb1 = discord.Embed(
                title=f"Ban System",
                description=f"The moderator {interaction.user.mention} has Ban you",
                color=discord.Colour.green(),
            ).add_field(name="Reason", value=f"{reason}",
            ).add_field(name="Duration", value=f"{time}",)

            emb2 = discord.Embed(
                title=f"Ban System",
                description=f"<:Failed:1080584797572833382> You don't have permission to ban any user {user.mention}",
                color=discord.Colour.red(),
            )

            if interaction.user.top_role <= user.top_role:
                await interaction.response.send_message(embed=emb2)
            elif interaction.user.top_role > user.top_role:
                db.execute("insert into tempban (user_id, time, guild_id) values (?,?,?)", (user.id, end_time, interaction.guild.id))
                db.commit()
                await interaction.response.send_message(embed=emb)
                await user.send(embed=emb1)
                await user.ban(reason=f"Banned by {interaction.user}")

        else:
            emb3 = discord.Embed(
                title=f"Ban System",
                description=f"<:Failed:1080584797572833382> You don't have permission to ban any user any user",
                color=discord.Colour.red(),
            )
            await interaction.response.send_message(embed=emb3)


    @app_commands.commands.command(name="unban", description="Unbans a user from the server")
    async def unban(self, interaction: discord.Interaction, user: discord.Member):
        


async def setup(bot: commands.Bot):
    await bot.add_cog(Ban(bot))
