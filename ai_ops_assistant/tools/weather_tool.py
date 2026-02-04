import os
import requests

class WeatherTool:
    def __init__(self):
        self.api_key = os.getenv("OPENWEATHER_API_KEY")
        self.base_url = "https://api.openweathermap.org/data/2.5/weather"

    def get_weather(self, city: str):
        """
        Fetches the current weather for a given city.
        """
        if not self.api_key:
            return {"error": "Missing OPENWEATHER_API_KEY"}

        try:
            params = {
                "q": city,
                "appid": self.api_key,
                "units": "metric"
            }
            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            weather = data.get("weather", [{}])[0].get("description", "Unknown")
            temp = data.get("main", {}).get("temp", "Unknown")
            
            return {
                "location": city,
                "temperature": f"{temp}°C",
                "condition": weather,
                "raw_data": data
            }
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}

if __name__ == "__main__":
    tool = WeatherTool()
    if tool.api_key:
        print(tool.get_weather("London"))
    else:
        print("Skipping weather test, no key.")
