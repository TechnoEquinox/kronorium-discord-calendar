#!/bin/bash
#
#
# Installs the requirements for kronorium-discord-calendar and sets up the enviorment

# COLOR CODES
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

PROJ_DIR="$HOME/kronorium-discord-calendar"
VENV_DIR="$HOME/kronorium-venv"
AUTH_JSON="$PROJ_DIR/auth.json"

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

# TODO: Define the systemd service file

echo -e "${GREEN}Install completed!${NC}"
echo "Configuring the bot..."

# Collect user input for Bot Token and Channel ID
echo -e "\nEnter your Discord Bot Token:"
read -r BOT_TOKEN
echo -e "Please enter the Channel ID where the bot should respond in:"
read -r CHANNEL_ID

# Create auth.json file
echo -e "{\n\t\"bot_token\": \"$BOT_TOKEN\",\n\t\"channel_id\": $CHANNEL_ID\n}" > "$AUTH_JSON"

echo -e "${GREEN}Setup completed!${NC}"
