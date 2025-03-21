import discord
from discord.ext import commands

# Function to read the bot token from a file
def get_token():
    with open("nekot.txt", "r") as file:
        return file.read().strip()

# Create an instance of the bot
bot = commands.Bot(command_prefix="awp.gg/")

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.command()
async def download(ctx):
    await ctx.send("Send the emoji you wanna download.")

@bot.event
async def on_message(message):
    # Ignore the bot's own messages
    if message.author == bot.user:
        return

    # Check if the message contains an emoji
    for emoji in message.content:
        if emoji.isemoji():
            if emoji in message.guild.emojis:  # Custom emoji
                custom_emoji = discord.utils.get(message.guild.emojis, name=emoji)
                if custom_emoji:
                    emoji_url = custom_emoji.url
                    await message.channel.send(f"Here is your download link: {emoji_url}")
                    return
            else:  # Unicode emoji
                await message.channel.send(f"Here is your download link for the emoji: https://twemoji.maxcdn.com/v/latest/72x72/{ord(emoji):x}.png")
                return

    await bot.process_commands(message)

# Get the bot token from the nekot.txt file and run the bot
bot.run(get_token())
