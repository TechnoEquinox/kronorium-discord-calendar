import json
import discord
from discord.ext import commands
from datetime import datetime
from helper import Helper

# Initialize the Helper class
helper = Helper()

# Load bot token and channel ID from auth.json
auth = helper.load_auth()

TOKEN = auth['bot_token']
CHANNEL_ID = int(auth['channel_id'])

# Load events from kronorium.json
events = helper.load_kronorium()

# Loads the config from config.json
config = helper.load_config()

# Set up the bot with the command prefix 'kron!' and intents
intents = discord.Intents.default()
intents.message_content = True  # Enables access to message content

bot = commands.Bot(command_prefix='kron!', intents=intents)

class CustomHelpCommand(commands.HelpCommand):
    def __init__(self, config):
        super().__init__()
        self.config = config

    async def send_bot_help(self, mapping):
        ctx = self.context
        response = f"Kronorium Discord Calendar\nVersion: {self.config['version']}\nCreated by: TechnoEquinox\n\n"
        response += "Commands:\n"
        for cog, commands in mapping.items():
            for command in commands:
                response += f"{command.name} - {command.help}\n"
        await ctx.send(f"```{response}```")

    async def send_command_help(self, command):
        ctx = self.context
        response = f"Help for command: {command.name}\n\n"
        response += f"{command.help}\n\n"
        response += f"Usage: {self.clean_prefix}{command.name} {command.signature}"
        await ctx.send(f"```{response}```")

    async def send_cog_help(self, cog):
        ctx = self.context
        response = f"Help for category: {cog.qualified_name}\n\n"
        for command in cog.get_commands():
            response += f"{command.name} - {command.help}\n"
        await ctx.send(f"```{response}```")

bot.help_command = CustomHelpCommand(config)

@bot.event
async def on_ready():
    print(f'Bot connected as {bot.user}')
    for guild in bot.guilds:
        print(f'- Bot is in guild: {guild.name} (id: {guild.id})')
        for channel in guild.channels:
            print(f'- - Channel: {channel.name} (id: {channel.id})')

@bot.command(help="Ping the bot to check if it's online.")
async def ping(ctx):
    print(f'Received ping command in channel {ctx.channel.id}')
    
    if ctx.channel.id == CHANNEL_ID:
        await ctx.send('Pong!')
    else:
        print(f'Ping command ignored in channel {ctx.channel.id}')

@bot.command(help="Get the events for today in Call of Duty Zombies history.")
async def today(ctx):
    print(f'Received today command in channel {ctx.channel.id}')
    
    if ctx.channel.id == CHANNEL_ID:
        response = helper.create_today_response(events)
        await ctx.send(response)
    else:
        print(f'Today command ignored in channel {ctx.channel.id}')

@bot.command(help="Show the configuration of the bot.")
async def config(ctx):
    print(f'Received config command in channel {ctx.channel.id}')

    if ctx.channel.id == CHANNEL_ID:
        response = helper.create_config_response()
        await ctx.send(response)
    else:
        print(f'Config command ignored in channel {ctx.channel.id}')

# Run the bot
bot.run(TOKEN)
