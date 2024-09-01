import json
import discord
import asyncio
import time
import os
from datetime import datetime
from helper import Helper

# Change working directory to the script's directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Initialize the Helper class
helper = Helper()

try:
    # Load bot token and channel ID from auth.json
    auth = helper.load_auth()
    
    TOKEN = auth['bot_token']
    CHANNEL_ID = int(auth['channel_id'])

    # Load events from kronorium.json
    events = helper.load_kronorium()

    intents = discord.Intents.default()
    intents.message_content = True  # Enables access to message content

    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f'Bot connected as {client.user} for cron job')
        channel = client.get_channel(CHANNEL_ID)
        if channel:
            start_time = time.time()  # Record the start time
            print(f"Sending today command to {channel}")

            response = helper.create_today_response(events)

            if response == "No events found for today.":
                print(f"{response}")
            else:
                end_time = time.time()  # Record the end time
                elapsed_time = helper.calc_elapsed_time(start_time, end_time)
                await channel.send(f"({elapsed_time}ms) " + response)
        else:
            print(f"Failed to get channel with ID {CHANNEL_ID}")

        # Update the bot's status with days until the next event value
        days = helper.days_until_next_event(events)
        status_message = f"{days} until the next event"
        await client.change_presence(activity=discord.Game(name=status_message))
        print(f"Set status: {status_message}")

        await client.close()  # Close the connection

    def run_bot():
        print("Running the bot's cronjob...")
        client.run(TOKEN)
        print("Bot finished running")

    if __name__ == "__main__":
        run_bot()

except Exception as e:
    print(f"Exception: {str(e)}")
