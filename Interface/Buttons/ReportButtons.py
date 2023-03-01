import discord
from discord.ui import View, button, Button
from discord import ButtonStyle

class ReportButtons(View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @button(style=ButtonStyle.red, emoji="✖", custom_id="delete_report")
    async def report_delete(self, interaction: discord.Interaction, button: Button):
        await interaction.response.defer()
        # mod_role = interaction.guild.get_role(1004051984640389141)
        # if mod_role in interaction.user.roles:
        await interaction.message.delete()
        # else:
        await interaction.followup.send(content="<:Failed:1080584797572833382> MissingPermissions, You aren't authorized to do that!", ephemeral=True)