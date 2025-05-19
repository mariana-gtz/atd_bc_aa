

class Utils:
    
    def get_current_date_in_timezone(timezone: str):
        """
        Returns the current date in a specified timezone.
        
        :param timezone: Timezone string (e.g., 'America/Chicago', 'Asia/Tokyo', 'Europe/London')
        :return: Formatted string with current date in the given timezone
        """
        try:
            TIMEZONE_MAP = {
                'CTS': 'America/Chicago',  # Central Time Zone (CST/CDT)
                'EST': 'America/New_York',
                'PST': 'America/Los_Angeles',
                'MST': 'America/Denver',
                'UTC': 'UTC',
            } 

            # Convert alias to full timezone name
            timezone = TIMEZONE_MAP.get(timezone, timezone)
            
            tz = pytz.timezone(timezone)
            current_time = datetime.now(tz)
            return current_time
        except pytz.UnknownTimeZoneError:
            return f"Error: Unknown timezone '{timezone}'"