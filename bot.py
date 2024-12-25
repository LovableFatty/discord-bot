import asyncio
import os
import discord 
from dotenv import load_dotenv
from discord.ext import commands
from commands.balances import BalanceCommands
from commands.quests import QuestCommands

# Load environment variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
USER_ID = int(os.getenv('USER_ID'))

# Set up the bot
intents = discord.Intents.default() 
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Event: Bot ready
@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    for guild in bot.guilds:
        print(f'Guild Name: {guild.name}')

# Main function to set up and run the bot
async def main():
    # Add cogs (commands modules)
    await bot.add_cog(BalanceCommands(bot, USER_ID))
    await bot.add_cog(QuestCommands(bot, USER_ID))

    # Start the bot
    await bot.start(TOKEN)

# Run the bot
if __name__ == "__main__":
    asyncio.run(main())
