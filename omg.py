import discord
from discord.ext import commands

# Function to read the bot token from a file
def get_token():
    with open("nekot.txt", "r") as file:
        return file.read().strip()

# Enable necessary intents
intents = discord.Intents.default()
intents.message_content = True  # Required for reading message content

# Create the bot instance with intents
bot = commands.Bot(command_prefix="awp.gg/", intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.command()
async def download(ctx):
    await ctx.send("Send the emoji you wanna download.")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # Detect custom emojis and extract their URL
    for word in message.content.split():
        if word.startswith("<:") and word.endswith(">"):  # Custom emoji format
            emoji_id = word.split(":")[-1].replace(">", "")  # Extract ID
            emoji_url = f"https://cdn.discordapp.com/emojis/{emoji_id}.png"
            await message.channel.send(f"Here is your download link: {emoji_url}")
            return

    await bot.process_commands(message)

# Run the bot using the token from nekot.txt
bot.run(get_token())  # <- Make sure nothing is written after this line
