import discord
from discord.ext import commands
import json

# Read the bot token from nekot.txt
with open("nekot.txt", "r") as f:
    TOKEN = f.read().strip()

# Read owner IDs from sdi1.txt and sdi2.txt
with open("sdi1.txt", "r") as f:
    owner_id1 = f.read().strip()

with open("sdi2.txt", "r") as f:
    owner_id2 = f.read().strip()

OWNER_IDS = [owner_id1, owner_id2]

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix=".", intents=intents)

# Load stock from file
try:
    with open("stock.json", "r") as f:
        stock = json.load(f)
except FileNotFoundError:
    stock = {}

def save_stock():
    with open("stock.json", "w") as f:
        json.dump(stock, f, indent=4)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.event
async def on_command_error(ctx, error):
    await ctx.send("That command doesn't exist! Use `.cmds` to view all commands.")

@bot.command()
async def stock(ctx):
    embed = discord.Embed(title="Stock", color=discord.Color.blue())
    for vp, amount in stock.items():
        embed.add_field(name=f"{vp}vp", value=f"```{amount}```", inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def restock(ctx, *, account: str):
    if str(ctx.author.id) not in OWNER_IDS:
        return
    try:
        mail_pass, vp = account.split("|")
        vp = vp.strip()
        if vp not in stock:
            stock[vp] = 0
        stock[vp] += 1
        with open(f"{vp}.txt", "a") as f:
            f.write(f"{mail_pass.strip()} | {vp}\n")
        save_stock()
        await ctx.send(f"Restocked {vp} VP!")
    except:
        await ctx.send("Invalid format! Use `.restock mail:pass | (number)vp`")

@bot.command()
async def with_(ctx, amount: str):
    if amount not in stock or stock[amount] == 0:
        await ctx.send("Needed restock!")
        return

    try:
        with open(f"{amount}.txt", "r") as f:
            lines = f.readlines()
        if not lines:
            await ctx.send("Needed restock!")
            return

        account = lines[0].strip()
        with open(f"{amount}.txt", "w") as f:
            f.writelines(lines[1:])
        
        stock[amount] -= 1
        save_stock()
        await ctx.send(f"Here's your account!\n```{account}```")
    except:
        await ctx.send("Error processing withdrawal.")

@bot.command()
async def cmds(ctx):
    await ctx.send(f"{ctx.author} just used .help!\n```\n"
                   ".stock - Show available stock\n"
                   ".with <amount> - Withdraw an account\n"
                   ".restock <mail:pass | (number)vp> - Add accounts to stock\n"
                   ".cmds - Display commands\n```")

bot.run(TOKEN)
