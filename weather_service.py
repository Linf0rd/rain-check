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
        self.db = get_db()  # May be None if database connection fails

    def get_weather_data(self, city):
        """Fetch weather data for a given city"""
        try:
            if not city:
                raise ValueError("City name cannot be empty")

            # Try to store search history if database is available
            if self.db:
                try:
                    search_history = SearchHistory(city=city)
                    self.db.add(search_history)
                    self.db.commit()
                except Exception:
                    # Ignore database errors and continue with weather data fetch
                    if self.db:
                        self.db.rollback()

            # Try to get cached data if database is available
            cached_data = None
            if self.db:
                try:
                    cached_data = self.db.query(WeatherCache).filter(
                        WeatherCache.city == city,
                        WeatherCache.timestamp > datetime.utcnow() - timedelta(minutes=30)
                    ).first()
                except Exception:
                    # Ignore cache errors and continue with fresh data fetch
                    if self.db:
                        self.db.rollback()

            if cached_data:
                return {
                    "current": cached_data.current_data,
                    "hourly": cached_data.hourly_data,
                    "daily": cached_data.daily_data
                }

            # Get coordinates
            geocoding_url = "https://api.openweathermap.org/geo/1.0/direct"
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
            forecast_params = current_params.copy()
            forecast_response = requests.get(f"{self.base_url}/forecast", params=forecast_params)
            if forecast_response.status_code == 401:
                raise ValueError("Invalid API key. Please check your OpenWeather API key.")
            forecast_response.raise_for_status()
            forecast_data = forecast_response.json()

            # Process forecast data
            hourly_data = forecast_data["list"][:8]  # Next 24 hours (3-hour intervals)
            daily_data = self._process_daily_from_forecast(forecast_data["list"])

            # Try to store in cache if database is available
            if self.db:
                try:
                    weather_cache = WeatherCache(
                        city=city,
                        lat=lat,
                        lon=lon,
                        current_data=current_data,
                        hourly_data=hourly_data,
                        daily_data=daily_data
                    )
                    self.db.add(weather_cache)
                    self.db.commit()
                except Exception:
                    # Ignore cache storage errors
                    if self.db:
                        self.db.rollback()

            return {
                "current": current_data,
                "hourly": hourly_data,
                "daily": daily_data
            }

        except requests.exceptions.RequestException as e:
            if "401" in str(e):
                raise ValueError("Invalid API key. Please check your OpenWeather API key.")
            raise Exception(f"Error fetching weather data: {str(e)}")
        except ValueError as e:
            raise ValueError(str(e))
        except Exception as e:
            raise Exception(f"An unexpected error occurred: {str(e)}")

    def process_hourly_forecast(self, data):
        """Process hourly forecast data"""
        try:
            df = pd.DataFrame([{
                'hour': datetime.fromtimestamp(item['dt']).strftime('%H:%M'),
                'temp': item['main']['temp'],
                'weather': item['weather']
            } for item in data['hourly']])

            df['temp'] = df['temp'].round(1)
            return df

        except Exception as e:
            raise Exception(f"Error processing hourly forecast: {str(e)}")

    def process_daily_forecast(self, data):
        """Process daily forecast data"""
        try:
            df = pd.DataFrame([{
                'day': datetime.fromtimestamp(item['dt']).strftime('%A'),
                'temp_day': item['main']['temp_max'],
                'temp_night': item['main']['temp_min'],
                'weather': item['weather']
            } for item in data['daily']])

            df['temp_day'] = df['temp_day'].round(1)
            df['temp_night'] = df['temp_night'].round(1)
            return df

        except Exception as e:
            raise Exception(f"Error processing daily forecast: {str(e)}")

    def _process_daily_from_forecast(self, forecast_list):
        """Process 5-day forecast data into daily format"""
        daily_data = []
        current_date = None

        for item in forecast_list:
            date = datetime.fromtimestamp(item['dt']).date()

            if date != current_date:
                temp_data = item['main']
                daily_data.append({
                    'dt': item['dt'],
                    'main': {
                        'temp_max': temp_data['temp_max'],
                        'temp_min': temp_data['temp_min'],
                        'temp': temp_data['temp']
                    },
                    'weather': item['weather']
                })
                current_date = date

                if len(daily_data) >= 7:
                    break

        return daily_data