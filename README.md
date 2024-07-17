# kronorium-discord-calendar
A Discord bot that tracks important Call of Duty Zombies dates from the Kronorium. When configured, the bot will ping a channel that you choose when the current date aligns with an event in the Kronorium. 

## Requirements
- A Debian Linux Server
- Access to the Discord Developers Portal
- Python 3 and pip

## Install

### Discord Setup
First, we must obtain a token from Discord for the bot. This token should never be shared and is unique to your instance. 

1. Log in to the [Discord Developer Portal](https://discord.com/developers/applications).
2. Create a new application called Kronorium, and agree to the Developers Terms of Service.
3. Add a description and avatar for the bot (feel free to use the bot_image.png file included in the project).
4. Under "Bot" > Copy down the token. If a token is not visible, reset the Token. You will only be able to see this once so make sure to put this somewhere safe. If you loose the token, you will have to regenerate another.
5. Under "OAuth2" > "OAuth2 URL Generator" > Select the "bot" option. This should reveal another menu. Add the permissions "Read Messages/View Channels" and "Send Messages". Copy the generated URL.
6. Paste the URL in your web browser and navigate to it. You will be asked to authenticate with Discord, and then you will select the Guild (Discord Server) you want to add the bot to.
7. The bot should now join your server, but should remain offline.

### Bot Setup
To clone the repository, run the following command in your terminal:

```sh
git clone https://github.com/TechnoEquinox/kronorium-discord-calendar.git
```
Navigate to the project directory and run the setup script:

```sh
cd kronorium-discord-calendar/
./install.sh
```
You may be asked to enter the sudo password during this process. This is just used to properly setup the systemd service. You will be asked to enter the following information:

| Prompt    | Explanation     |
|--------------|--------------|
| Discord Bot Token | The token created on the Discord Developer Portal |
| Channel ID | This is the ID for the discord channel where you want your bot to respond. This can be found in Discord by right clicking on the channel and selecting "Copy Channel ID". |
| Daily Ping | Yes/No if you want to recieve a ping in the specified channel on a day that matches a day in the Kronorium. If the day doesn't math, no ping will be sent. |
| Ping Hour | This is the hour of the day you want the daily ping to come (An integer from 0 - 23). |

Once this information has been entered, a service is created and the setup is complete. 

## Changing the Configuration
There are two main configuration files: auth.json and config.json that are created with the install script. 

Should you want to make any changes after the installation, you can configure the Token and Channel IDs in auth.json. Should you want to change any other options, you can find them in config.json. 

After making any changes to either of these files, you will need to restart the service:

```sh
sudo systemctl restart kronorium-discord-calendar.service
```







