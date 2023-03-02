import discord, sqlite3, datetime
from discord.ext import commands, tasks

db = sqlite3.connect('db.db')

class Ban(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.check_bans.start()

    def cog_unload(self):
        self.check_bans.cancel()

    @tasks.loop(seconds=1)
    async def check_bans(self):
        now = int(datetime.datetime.utcnow().timestamp())
        rows = self.db.execute("SELECT * FROM tempban WHERE end_time >= ?", (now,))
        r1 = rows.fetchall()
        for row in r1:
            try:
                print(row[0])
                user = await self.client.fetch_user(row[0])
                guild = self.client.get_guild(config.guild)
                await guild.unban(user)
                self.db.execute("DELETE FROM tempban WHERE user_id = ?, guild_id", (row[0], row[0][0]))
                self.db.commit()
            except discord.NotFound:
                print(f"Could not find user with ID {row[0]}")   


async def setup(bot: commands.Bot):
    await bot.add_cog(Ban(bot))
