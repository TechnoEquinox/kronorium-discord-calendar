import json
import discord
from discord.ext import commands
from datetime import datetime

# Load bot token and channel ID from auth.json
with open('auth.json', 'r') as f:
    auth = json.load(f)

TOKEN = auth['bot_token']
CHANNEL_ID = int(auth['channel_id'])

# Load events from kronorium.json
with open('kronorium.json', 'r') as f:
    events = json.load(f)

# Set up the bot with the command prefix 'kron!' and intents
intents = discord.Intents.default()
intents.message_content = True  # Enables access to message content

bot = commands.Bot(command_prefix='kron!', intents=intents)

@bot.event
async def on_ready():
    print(f'Bot connected as {bot.user}')
    guild = bot.guilds[0]
    print(f'Bot is in guild: {guild.name} (id: {guild.id})')

@bot.command()
async def ping(ctx):
    print(f'Received ping command in channel {ctx.channel.id}')
    if ctx.channel.id == CHANNEL_ID:
        await ctx.send('Pong!')
    else:
        print(f'Ping command ignored in channel {ctx.channel.id}')

@bot.command()
async def event(ctx, event_id: str):
    print(f'Received event command for ID {event_id} in channel {ctx.channel.id}')
    if ctx.channel.id == CHANNEL_ID:
        event = next((event for event in events if event['ID'] == event_id), None)
        if event:
            response = f"**{event['Title']}**\n{event['Description']}\nMap Association: {event['MapAssociation']}\nDate: {event['Date']}"
            await ctx.send(response)
        else:
            await ctx.send(f"No event found with ID {event_id}.")
    else:
        print(f'Event command ignored in channel {ctx.channel.id}')

@bot.command()
async def today(ctx):
    print(f'Received today command in channel {ctx.channel.id}')
    if ctx.channel.id == CHANNEL_ID:
        today = datetime.now().strftime("%m-%d")
        found_events = [event for event in events if datetime.strptime(event['Date'], "%Y-%m-%d").strftime("%m-%d") == today]
        if found_events:
            response = "```Today in Zombies History\n\n"
            for event in found_events:
                date = datetime.strptime(event['Date'], "%Y-%m-%d").strftime("%B %d, %Y")
                map_association = f" ({event['Map']})" if event['Map'] != "None" else ""
                description = event['Description']
                response += f"-----{date}-----\n{map_association}\n{description}\n\n"
            response += "```"
            await ctx.send(response)
        else:
            await ctx.send("No events found for today.")
    else:
        print(f'Today command ignored in channel {ctx.channel.id}')


# Run the bot
bot.run(TOKEN)
