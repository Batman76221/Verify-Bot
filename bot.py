import discord
from discord.ext import commands
import json

with open("config.json") as f:
    config = json.load(f)

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

@bot.event
async def on_ready():
    await bot.load_extension("commands.verify")
    await bot.tree.sync()
    print(f"Logged in as {bot.user}")

bot.run(config["token"])
