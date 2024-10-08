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
    
    def calc_elapsed_time(self, start, end):
        """
            Takes a start and end time and calculates the time in miliseconds (ms) that have elapsed
            Returns: int
        """
        return round((end - start) * 1000, 0)  # Elapsed time in ms
    
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
        time_for_ping = self.convert_hour_to_time(config['tod'])
        
        response = f"kronorium-discord-calendar\nVersion: {config['version']}\nCreated by: TechnoEquinox\n\n"
        response += f"Daily Ping Enabled: {config['daily_ping']}\nTime for ping: {time_for_ping}\nPrefix: kron!\n\n"
        response += "A special thanks to Psy for finding that one bug that I completely missed."

        return f"```{response}```"
    
    def convert_hour_to_time(self, hour):
        """
            Function to convert hour integer to a readable time format
            Returns: String
        """
        if hour == -1:
            return "Unknown"
        
        period = "am" if hour < 12 else "pm"
        hour_display = hour % 12
        hour_display = 12 if hour_display == 0 else hour_display
        
        return f"{hour_display}:00{period}"
    
    def days_until_next_event(self, events):
        """
            Function that takes a list of events from our kronorium.json, and calculates the amount of days between
            today and that date
            Returns: int
        """
        today = datetime.now().date()  # Get the current date
        sorted_events = sorted(events, key=lambda x: datetime.strptime(x['Date'], "%Y-%m-%d").replace(year=today.year))

        for event in sorted_events:
            event_date = datetime.strptime(event['Date'], "%Y-%m-%d").replace(year=today.year).date()
            
            if event_date > today:  # The event must be strictly after today
                return (event_date - today).days

        # If all events are past, consider the first event of the next year
        next_year_first_event = datetime.strptime(sorted_events[0]['Date'], "%Y-%m-%d").replace(year=today.year + 1).date()
        return (next_year_first_event - today).days
