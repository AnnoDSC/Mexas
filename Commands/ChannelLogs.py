import discord, sqlite3, config
from discord.ext import commands
from discord import app_commands

db = sqlite3.connect('db.db')

class ChannelLogs(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot


    @app_commands.commands.command(name="channellogs", description="List the newest channellogs from the bot")
    async def channellogs(self, interaction: discord.Interaction):
        changelog_embed = discord.Embed(
            colour=discord.Color.green()
        ).set_author(name=f'Channellogs {config.MEXAS_VERSION}', icon_url='https://i.imgur.com/l9bQYxS.png'
        ).set_thumbnail(url=f'https://i.imgur.com/l9bQYxS.png'
        ).add_field(name="**- Completed**", value="- Finish Ban command with a normal ban and temporary ban", inline=False
        ).set_footer(text=f'{config.MEXAS_VERSION} | By Annodsc')
        await interaction.response.send_message(embed=changelog_embed)





async def setup(bot: commands.Bot):
    await bot.add_cog(ChannelLogs(bot))
