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

# Set up the bot with the command prefix 'kron!' and intents
intents = discord.Intents.default()
intents.message_content = True  # Enables access to message content

bot = commands.Bot(command_prefix='kron!', intents=intents)

@bot.event
async def on_ready():
    print(f'Bot connected as {bot.user}')
    for guild in bot.guilds:
        print(f'- Bot is in guild: {guild.name} (id: {guild.id})')
        for channel in guild.channels:
            print(f'- - Channel: {channel.name} (id: {channel.id})')

@bot.command()
async def ping(ctx):
    print(f'Received ping command in channel {ctx.channel.id}')
    
    if ctx.channel.id == CHANNEL_ID:
        await ctx.send('Pong!')
    else:
        print(f'Ping command ignored in channel {ctx.channel.id}')

@bot.command()
async def today(ctx):
    print(f'Received today command in channel {ctx.channel.id}')
    
    if ctx.channel.id == CHANNEL_ID:
        response = helper.create_today_response(events)
        await ctx.send(response)
    else:
        print(f'Today command ignored in channel {ctx.channel.id}')

@bot.command()
async def config(ctx):
    print(f'Received config command in channel {ctx.channel.id}')

    if ctx.channel.id == CHANNEL_ID:
        response = helper.create_config_response()
        await ctx.send(response)
    else:
        print(f'Config command ignored in channel {ctx.channel.id}')

# Run the bot
bot.run(TOKEN)
