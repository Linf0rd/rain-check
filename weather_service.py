import requests
import os
from datetime import datetime, timedelta
import pandas as pd
from sqlalchemy.orm import Session
from database import get_db, SearchHistory, WeatherCache

class WeatherService:
    def __init__(self):
        self.api_key = os.getenv("OPENWEATHER_API_KEY")
        if not self.api_key:
            raise ValueError("OpenWeather API key not found. Please set the OPENWEATHER_API_KEY environment variable.")
        self.base_url = "https://api.openweathermap.org/data/2.5"
        self.db = next(get_db())

    def get_weather_data(self, city):
        """Fetch weather data for a given city"""
        try:
            if not city:
                raise ValueError("City name cannot be empty")

            # Store search history
            search_history = SearchHistory(city=city)
            self.db.add(search_history)
            self.db.commit()

            # Check cache first
            cached_data = self.db.query(WeatherCache).filter(
                WeatherCache.city == city,
                WeatherCache.timestamp > datetime.utcnow() - timedelta(minutes=30)
            ).first()

            if cached_data:
                return {
                    "current": cached_data.current_data,
                    "hourly": cached_data.hourly_data,
                    "daily": cached_data.daily_data
                }

            # Get coordinates
            geocoding_url = f"https://api.openweathermap.org/geo/1.0/direct"
            params = {
                "q": city,
                "limit": 1,
                "appid": self.api_key
            }
            location_response = requests.get(geocoding_url, params=params)
            if location_response.status_code == 401:
                raise ValueError("Invalid API key. Please check your OpenWeather API key.")
            location_response.raise_for_status()
            location = location_response.json()

            if not location:
                raise ValueError(f"City '{city}' not found")

            lat, lon = location[0]['lat'], location[0]['lon']

            # Get current weather
            current_params = {
                "lat": lat,
                "lon": lon,
                "appid": self.api_key,
                "units": "metric"
            }
            current_response = requests.get(f"{self.base_url}/weather", params=current_params)
            if current_response.status_code == 401:
                raise ValueError("Invalid API key. Please check your OpenWeather API key.")
            current_response.raise_for_status()
            current_data = current_response.json()

            # Get forecast data
            forecast_params = {
                "lat": lat,
                "lon": lon,
                "appid": self.api_key,
                "units": "metric"
            }
            forecast_response = requests.get(f"{self.base_url}/forecast", params=forecast_params)
            if forecast_response.status_code == 401:
                raise ValueError("Invalid API key. Please check your OpenWeather API key.")
            forecast_response.raise_for_status()
            forecast_data = forecast_response.json()

            # Store in cache
            weather_cache = WeatherCache(
                city=city,
                lat=lat,
                lon=lon,
                current_data=current_data,
                hourly_data=forecast_data["list"][:8],
                daily_data=self._process_daily_from_forecast(forecast_data["list"])
            )
            self.db.add(weather_cache)
            self.db.commit()

            # Return combined data
            return {
                "current": current_data,
                "hourly": forecast_data["list"][:8],
                "daily": self._process_daily_from_forecast(forecast_data["list"])
            }

        except requests.exceptions.RequestException as e:
            if "401" in str(e):
                raise ValueError("Invalid API key. Please check your OpenWeather API key.")
            raise Exception(f"Error fetching weather data: {str(e)}")
        except ValueError as e:
            raise ValueError(str(e))
        except Exception as e:
            raise Exception(f"An unexpected error occurred: {str(e)}")

    def _process_daily_from_forecast(self, forecast_list):
        """Process 5-day forecast data into daily format"""
        daily_data = []
        current_date = None

        for item in forecast_list:
            date = datetime.fromtimestamp(item['dt']).date()

            if date != current_date:
                daily_data.append({
                    'dt': item['dt'],
                    'temp': {
                        'day': item['main']['temp'],
                        'night': item['main']['temp_min']
                    },
                    'weather': item['weather']
                })
                current_date = date

                if len(daily_data) >= 7:
                    break

        return daily_data

    def process_hourly_forecast(self, data):
        """Process hourly forecast data"""
        try:
            hourly = data['hourly']  # Next 24 hours (3-hour intervals)
            df = pd.DataFrame([{
                'dt': item['dt'],
                'temp': item['main']['temp'],
                'weather': item['weather']
            } for item in hourly])

            df['datetime'] = pd.to_datetime(df['dt'], unit='s')
            df['hour'] = df['datetime'].dt.strftime('%H:%M')
            df['temp'] = df['temp'].round(1)
            return df[['hour', 'temp', 'weather']]
        except Exception as e:
            raise Exception(f"Error processing hourly forecast: {str(e)}")

    def process_daily_forecast(self, data):
        """Process daily forecast data"""
        try:
            daily = data['daily']  # Next 7 days
            df = pd.DataFrame(daily)
            df['datetime'] = pd.to_datetime(df['dt'], unit='s')
            df['day'] = df['datetime'].dt.strftime('%A')
            df['temp_day'] = df['temp'].apply(lambda x: round(x['day'], 1))
            df['temp_night'] = df['temp'].apply(lambda x: round(x['night'], 1))
            return df[['day', 'temp_day', 'temp_night', 'weather']]
        except Exception as e:
            raise Exception(f"Error processing daily forecast: {str(e)}")