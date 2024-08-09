#!/bin/bash
#
#
# Installs the requirements for kronorium-discord-calendar and sets up the enviorment

# COLOR CODES
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

VERSION="1.0-beta.2"
PROJ_DIR="$HOME/kronorium-discord-calendar"
VENV_DIR="$HOME/kronorium-venv"
AUTH_JSON="$PROJ_DIR/auth.json"
CONFIG_JSON="$PROJ_DIR/config.json"
SERVICE_FILE="/etc/systemd/system/kronorium-discord-calendar.service"

echo "kronorium-discord-calendar Installer"
echo -e "Created by: TechnoEquinox\tCreated on: 07-14-2024"

echo -e "\nVerifying cron installation..."
if command -v cron >/dev/null 2>&1 || command -v crond >/dev/null 2>&1; then
    echo -e "${GREEN}Cron is installed.${NC}"
else
    echo -e "${YELLOW}Cron is not installed. Installing it now...${NC}"
    sudo apt-get install cron
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}Successfully installed cron.${NC}"
    else
        echo -e "${RED}ERROR: Failed to install cron.${NC}"
        exit 1
    fi
fi

echo -e "Verifying kronorium-discord-calendar files..."
if [ -d "$PROJ_DIR" ]; then
    echo -e "${GREEN}Successfully verified kronorium-discord-calendar files.${NC}"
else
    echo -e "${RED}ERROR: Verification of kronorium-discord-calendar files failed.${NC}"
    exit 1
fi

# venv and Python package installation
echo "Checking if Python venv already exists in $HOME ..."
if [ -d "$VENV_DIR" ]; then
    echo -e "${YELLOW}Python venv already exists. No changes made.${NC}"
else
    echo -e "${YELLOW}Python venv does not exist. Creating it now...${NC}"
    python3 -m venv "$VENV_DIR"
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}Successfully created Python venv.${NC}"
        echo "Activating virtual environment..."
        source "$VENV_DIR/bin/activate"
        if [ $? -eq 0 ]; then
            echo -e "${GREEN}Successfully activated virtual environment.${NC}"
            echo "Installing required Python packages..."
            pip install -r "$PROJ_DIR/requirements.txt"
            if [ $? -eq 0 ]; then
                echo -e "${GREEN}Successfully installed required Python packages.${NC}"
            else
                echo -e "${RED}ERROR: Failed to install required Python packages.${NC}"
                deactivate
                exit 1
            fi
            deactivate
        else
            echo -e "${RED}ERROR: Failed to activate virtual environment.${NC}"
            exit 1
        fi
    else
        echo -e "${RED}ERROR: Failed to create Python venv.${NC}"
        exit 1
    fi
fi

echo -e "${GREEN}Install completed!${NC}"
echo "Configuring the bot..."

# Check if auth.json exists
if [ -f "$AUTH_JSON" ]; then
    echo -e "${YELLOW}auth.json already exists. Skipping bot token and channel ID configuration.${NC}"
else
    # Collect user input for Bot Token and Channel ID
    echo -e "\nEnter your Discord Bot Token:"
    read -r BOT_TOKEN
    echo -e "Please enter the Channel ID where the bot should respond in:"
    read -r CHANNEL_ID

    # Create auth.json file
    echo -e "{\n\t\"bot_token\": \"$BOT_TOKEN\",\n\t\"channel_id\": $CHANNEL_ID\n}" > "$AUTH_JSON"
fi

# Check if config.json exists
if [ -f "$CONFIG_JSON" ]; then
    echo -e "${YELLOW}config.json already exists. Skipping daily ping configuration.${NC}"
else
    # Create the config.json file
    read -p "Do you want to receive a daily ping in $CHANNEL_ID? (yes/no): " daily_ping_answer

    if [[ "$daily_ping_answer" == "yes" ]]; then
        read -p "Enter the hour (0-23) you want to have the bot ping the channel: " tod
        while [[ ! "$tod" =~ ^[0-9]+$ ]] || [ "$tod" -lt 0 ] || [ "$tod" -gt 23 ]; do
            echo -e "${RED}Invalid input. Please enter a number between 0 and 23.${NC}"
            read -p "Enter the hour (0-23) you want to have the bot ping the channel: " tod
        done
        daily_ping=true
    else
        daily_ping=false
        tod=-1
    fi
    
    # Prompt for the prefix string
    read -p "Enter the command prefix (default: kron!): " prefix
    if [ -z "$prefix" ]; then
        prefix="kron!"
    else
        while [[ ! "$prefix" =~ ^[a-zA-Z]{1,4}!$ ]]; do
            echo -e "${RED}Invalid input. The prefix must be 1-4 alphabetic characters followed by an exclamation mark (!).${NC}"
            read -p "Enter the command prefix (default: kron!): " prefix
            if [ -z "$prefix" ]; then
                prefix="kron!"
                break
            fi
        done
    fi

    echo -e "{\n\t\"version\": \"$VERSION\",\n\t\"daily_ping\": $daily_ping,\n\t\"prefix\": \"$prefix\",\n\t\"tod\": $tod\n}" > "$CONFIG_JSON"
fi


echo "Checking if the kronorium-discord-calendar service exists..."
if [ -f "$SERVICE_FILE" ]; then
    echo -e "${YELLOW}Systemd service already exists. Skipping creation.${NC}"
else
    # Create systemd service file
    echo -e "${YELLOW}Systemd service not found. Creating the service...${NC}"
    sudo bash -c "cat > $SERVICE_FILE" <<EOL
[Unit]
Description=Kronorium Discord Calendar Bot
After=network.target

[Service]
User=$USER
WorkingDirectory=$PROJ_DIR
ExecStart=$VENV_DIR/bin/python3 $PROJ_DIR/bot.py
Restart=always

[Install]
WantedBy=multi-user.target
EOL

    # Enable and start the systemd service
    sudo systemctl daemon-reload
    sudo systemctl enable kronorium-discord-calendar.service
    sudo systemctl start kronorium-discord-calendar.service
fi

# Add cron job for daily ping
if [ "$daily_ping" = true ]; then
    CRON_JOB="0 $tod * * * $VENV_DIR/bin/python3 $PROJ_DIR/cronjob.py >> $PROJ_DIR/logs/cronjob.log 2>&1"
    # Check if the cron job already exists
    (crontab -l 2>/dev/null | grep -F "$CRON_JOB") || (crontab -l 2>/dev/null; echo "$CRON_JOB") | crontab -
fi

echo -e "${GREEN}Setup completed!${NC}"