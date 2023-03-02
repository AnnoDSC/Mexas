import traceback
import discord
from Interface.Buttons.ReportButtons import ReportButtons

class BugReport(discord.ui.Modal, title="Report"):
    heading = discord.ui.TextInput(
        label="Title of your report",
        style=discord.TextStyle.short,
        placeholder="Type the title of your report, i.e Commands not working",
        required=True,
        max_length=30
    )

    report = discord.ui.TextInput(
        label="Tell us what you want to report",
        style=discord.TextStyle.long,
        placeholder="Describe your issue in detail",
        required=True,
        max_length=1000
    )

    async def on_submit(self, interaction: discord.Interaction):
        channel = interaction.client.get_channel(1080580881741271150)

        suggestion_embed = discord.Embed(
            title=self.heading,
            description=self.report,
            color=discord.Color.magenta()
        )
        suggestion_embed.set_author(name=interaction.user, icon_url=interaction.user.avatar)
        suggestion_embed.set_thumbnail(url=interaction.guild.icon)
        suggestion_embed.set_footer(text=f"Sent from, Guild: {interaction.guild.name} | Members: {interaction.guild.member_count}")

        await channel.send(embed=suggestion_embed, view=ReportButtons())
        await interaction.response.send_message("<:Done:1080584760616820766> Your report has been sent!", ephemeral=True)
        return

    async def on_error(self, interaction: discord.Interaction, error: Exception):
        await interaction.response.send_message("<:Failed:1080584797572833382> Oops! Something went wrong.", ephemeral=True)
        print(error)