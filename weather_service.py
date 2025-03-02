import requests
import os
from datetime import datetime
import pandas as pd

class WeatherService:
    def __init__(self):
        self.api_key = os.getenv("OPENWEATHER_API_KEY", "your_default_key")
        self.base_url = "http://api.openweathermap.org/data/2.5"
        
    def get_weather_data(self, city):
        """Fetch weather data for a given city"""
        try:
            # Get coordinates
            geocoding_url = f"http://api.openweathermap.org/geo/1.0/direct"
            params = {
                "q": city,
                "limit": 1,
                "appid": self.api_key
            }
            location = requests.get(geocoding_url, params=params).json()
            
            if not location:
                return None
                
            lat, lon = location[0]['lat'], location[0]['lon']
            
            # Get weather data
            weather_url = f"{self.base_url}/onecall"
            params = {
                "lat": lat,
                "lon": lon,
                "appid": self.api_key,
                "units": "metric",
                "exclude": "minutely"
            }
            
            response = requests.get(weather_url, params=params)
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error fetching weather data: {str(e)}")
            
    def process_hourly_forecast(self, data):
        """Process hourly forecast data"""
        hourly = data['hourly'][:24]  # Next 24 hours
        df = pd.DataFrame(hourly)
        df['datetime'] = pd.to_datetime(df['dt'], unit='s')
        df['hour'] = df['datetime'].dt.strftime('%H:%M')
        df['temp'] = df['temp'].round(1)
        return df[['hour', 'temp', 'weather']]
        
    def process_daily_forecast(self, data):
        """Process daily forecast data"""
        daily = data['daily'][:7]  # Next 7 days
        df = pd.DataFrame(daily)
        df['datetime'] = pd.to_datetime(df['dt'], unit='s')
        df['day'] = df['datetime'].dt.strftime('%A')
        df['temp_day'] = df['temp'].apply(lambda x: round(x['day'], 1))
        df['temp_night'] = df['temp'].apply(lambda x: round(x['night'], 1))
        return df[['day', 'temp_day', 'temp_night', 'weather']]
