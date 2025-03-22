import discord
import random
import os

from discord.ext import commands

TOKEN_FILE = "neket.txt"

def get_token():
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "r") as f:
            return f.read().strip()
    token = input("Enter your bot token: ").strip()
    with open(TOKEN_FILE, "w") as f:
        f.write(token)
    return token

def generate_links(amount):
    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    return [f"https://prnt.sc/{''.join(random.choices(chars, k=6))}" for _ in range(amount)]

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True

bot = commands.Bot(command_prefix=["+", "-", "$"], intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.command()
async def links(ctx):
    await ctx.send("How much links u want?")

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel and m.content.isdigit()
    
    try:
        msg = await bot.wait_for("message", check=check, timeout=30)
        amount = int(msg.content)
        links_list = generate_links(amount)

        embed = discord.Embed(title="Links", description="```\n" + "\n".join(links_list) + "```", color=discord.Color.light_grey())
        await ctx.send(embed=embed)
    except:
        await ctx.send("Invalid input or timeout.")

@bot.command()
async def stop(ctx):
    await ctx.send("Shutting down...")
    await bot.close()

bot.run(get_token())
