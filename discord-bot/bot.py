import discord
from discord.ext import commands
import asyncio

TOKEN = "MTQxNTMxNDc4MDkyNjkwMjM1Mw.Gx5TMU.n0qctGpgJv8N71PqndEo6uzkd2UeAr4A-Lw-BM"
bot = commands.Bot(command_prefix = '!',intents=discord.Intents.all())

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

@bot.command()
async def ping(ctx):
    await ctx.send("PONG")

@bot.command()
async def greet(ctx):
    await ctx.send("Hello! 👋 I'm your AI assistant. How can I help you today?")

@bot.command()
async def helpme(ctx):
    await ctx.send(
        "Here are some things I can do right now:\n"
        "🔹 `!ping` → Check if I'm alive\n"
        "🔹 `!greet` → Get a friendly greeting\n"
        "🔹 `!weather` → Dummy weather info\n"
        "🔹 `!joke` → I'll tell you a joke\n"
        "🔹 `!shutdown` → (Owner only) Shut me down"
    )

@bot.command()
async def weather(ctx):
    await ctx.send("☀️ It's sunny and 27°C outside! (Hardcoded for now)")

@bot.command()
async def joke(ctx):
    await ctx.send("😂 Why don't programmers like nature? Too many *bugs*!")


@bot.command()
@commands.is_owner()
async def shutdown(ctx):
    await ctx.send("Shutting down... 👋")
    await bot.close()

bot.run(TOKEN)