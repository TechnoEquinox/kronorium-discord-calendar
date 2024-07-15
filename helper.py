from datetime import datetime
import json

class Helper():
    def __init__(self):
        pass

    def load_auth(self):
        """
            Loads the data from auth.json.
            Returns: dict()
        """

        with open('auth.json', 'r') as f:
            return json.load(f)
    
    def load_kronorium(self):
        """
            Loads the data from kronorium.json
            Returns: dict()
        """

        with open('kronorium.json', 'r') as f:
            return json.load(f)
    
    def load_config(self):
        """
            Loads the data from config.json
            Returns: dict()
        """

        with open('config.json', 'r') as f:
            return json.load(f)
    
    def create_today_response(self, events):
        """
            Creates the response for the 'today' command.
            Returns: String
        """

        today = datetime.now().strftime("%m-%d")
        found_events = [event for event in events if datetime.strptime(event['Date'], "%Y-%m-%d").strftime("%m-%d") == today]
        
        if found_events:
            response = "Today in Call of Duty Zombies History\n\n"
            for event in found_events:
                date = datetime.strptime(event['Date'], "%Y-%m-%d").strftime("%B %d, %Y")
                map_association = f"Map: {event['Map']}\n" if event['Map'] != "None" else ""
                description = event['Description']
                
                response += f"|----- {date} -----|\n"
                if map_association != "":
                    response += f"\n{map_association}\n"
                
                response += f"\n- {description}\n\n"
                
            return f"```{response}```"
        else:
            return "No events found for today."
    
    def create_config_response(self):
        """
            Creates the response for the 'config' command.
            Returns: String
        """
        config = self.load_config()
        
        response = f"kronorium-discord-calendar\nVersion: {config['version']}\nCreated by: TechnoEquinox\n\n"
        response += f"Daily Ping Enabled: {config['daily_ping']}\nTime for ping: {config['tod']}\nPrefix: kron!\n\n"

        return f"```{response}```"
