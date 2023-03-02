import discord, os, config, sys, sqlite3
from discord.ext import commands

db = sqlite3.connect("db.db")

sys.dont_write_bytecode = True

intents = discord.Intents.default()
intents.message_content = True

class Mexas(commands.AutoShardedBot):
    def __init__(self):
        super().__init__(
            command_prefix=config.MEXAS_PREFIX,
            intents=intents,
            status=discord.Status.dnd,
            activity=discord.Game(name=f"/help | {config.MEXAS_VERSION}"),
        )

    async def setup_hook(self):
        for filename in os.listdir("./Commands"):
            if filename.endswith('.py'):
                await self.load_extension(f"Commands.{filename[:-3]}")
                print(f"Loaded {filename} ✅")
            
            if filename.startswith('__'):
                pass
        
        for filename in os.listdir("./Events"):
            if filename.endswith('.py'):
                await self.load_extension(f"Events.{filename[:-3]}")
                print(f"Loaded {filename} ✅")
            
            if filename.startswith('__'):
                pass
        
        for filename in os.listdir("./Tasks"):
            if filename.endswith('.py'):
                await self.load_extension(f"Tasks.{filename[:-3]}")
                print(f"Loaded {filename} ✅")
            
            if filename.startswith('__'):
                pass
        
        await bot.tree.sync()


bot = Mexas()

def cc_db():
    db.execute("create table if not exists reports (id integer, upvote integer, downvote integer)")
    db.execute("create table if not exists tempban (user_id integer, time integer, guild_id integer)")
    db.commit()

@bot.event
async def on_ready():
    cc_db()
    print("--------------------------------")
    print(f"{bot.user} is connected to Discord, current latency is {round(bot.latency * 1000)}ms")
    print("--------------------------------")

@bot.command(name="reload")
@commands.is_owner()
async def reload(ctx: commands.Context, folder:str, cog:str):
    # Reloads the file, thus updating the Cog class.
    await bot.reload_extension(f"{folder}.{cog}")
    await ctx.send(f"🔁 {cog} reloaded!")

@bot.command(name="load")
@commands.is_owner()
async def load(ctx: commands.Context, folder:str, cog:str):
    # Reloads the file, thus updating the Cog class.
    await bot.load_extension(f"{folder}.{cog}")
    await ctx.send(f"🆙 {cog} loaded!")


bot.run(config.MEXAS_TOKEN)