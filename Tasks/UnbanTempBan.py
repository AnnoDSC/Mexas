import discord, sqlite3, datetime
from discord.ext import commands, tasks

db = sqlite3.connect('db.db')

class UnbanTempBan(commands.Cog):
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
        rows = db.execute("SELECT * FROM tempban WHERE time <= ?", (now,))
        r1 = rows.fetchall()
        for user_id, time, guild_id in r1:
            try:
                user = await self.bot.fetch_user(user_id)
                guild = self.bot.get_guild(guild_id)
                await guild.unban(user)
                db.execute("DELETE FROM tempban WHERE user_id = ?", (user_id,))
                db.commit()
            except discord.NotFound:
                pass 


async def setup(bot: commands.Bot):
    await bot.add_cog(UnbanTempBan(bot))
