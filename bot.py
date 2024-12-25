import os
from dotenv import load_dotenv
from discord.ext import commands
from commands import balances, quests
from database import init_db

# Load environment variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
USER_ID = int(os.getenv('USER_ID'))

# Set up the bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Initialize the database
init_db()

# Load commands
bot.add_cog(balances.BalanceCommands(bot, USER_ID))
bot.add_cog(quests.QuestCommands(bot, USER_ID))

# Event: Bot ready


@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    for guild in bot.guilds:
        print(f'Guild Name: {guild.name}')

# Run the bot
bot.run(TOKEN)
