import streamlit as st
import pandas as pd
from weather_service import WeatherService
from visualization import create_hourly_temp_chart, create_daily_temp_chart
from styles import apply_custom_styles, get_weather_icon

# Page configuration
st.set_page_config(
    page_title="Weather Forecast",
    page_icon="🌤️",
    layout="wide"
)

# Apply custom styles
apply_custom_styles()

try:
    # Initialize weather service
    weather_service = WeatherService()

    # Header
    st.title("📱 Weather Forecast")
    st.markdown("Get detailed weather forecasts for any location")

    # Search bar
    city = st.text_input("Enter city name", "London")

    # Add Font Awesome
    st.markdown("""
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">
    """, unsafe_allow_html=True)

    if city:
        try:
            with st.spinner("Fetching weather data..."):
                weather_data = weather_service.get_weather_data(city)

                # Current weather
                current = weather_data['current']
                col1, col2, col3 = st.columns(3)

                with col1:
                    st.markdown(f"""
                        <div class="weather-card">
                            <i class="{get_weather_icon(current['weather'][0]['main'])} weather-icon"></i>
                            <div class="temp-text">{round(current['main']['temp'])}°C</div>
                            <div class="condition-text">{current['weather'][0]['description'].capitalize()}</div>
                        </div>
                    """, unsafe_allow_html=True)

                with col2:
                    st.markdown(f"""
                        <div class="weather-card">
                            <i class="fas fa-tint weather-icon"></i>
                            <div class="temp-text">{current['main']['humidity']}%</div>
                            <div class="condition-text">Humidity</div>
                        </div>
                    """, unsafe_allow_html=True)

                with col3:
                    st.markdown(f"""
                        <div class="weather-card">
                            <i class="fas fa-wind weather-icon"></i>
                            <div class="temp-text">{round(current['wind']['speed'])} m/s</div>
                            <div class="condition-text">Wind Speed</div>
                        </div>
                    """, unsafe_allow_html=True)

                # Hourly forecast
                st.subheader("Hourly Forecast")
                hourly_data = weather_service.process_hourly_forecast({"hourly": weather_data['hourly']})
                st.plotly_chart(create_hourly_temp_chart(hourly_data), use_container_width=True)

                # Daily forecast
                st.subheader("7-Day Forecast")
                daily_data = weather_service.process_daily_forecast({"daily": weather_data['daily']})
                st.plotly_chart(create_daily_temp_chart(daily_data), use_container_width=True)

                # Detailed daily forecast
                st.subheader("Detailed Daily Forecast")
                for _, row in daily_data.iterrows():
                    col1, col2 = st.columns([1, 3])
                    with col1:
                        st.markdown(f"""
                            <div class="weather-card">
                                <div style="font-weight: bold">{row['day']}</div>
                                <i class="{get_weather_icon(row['weather'][0]['main'])} weather-icon"></i>
                            </div>
                        """, unsafe_allow_html=True)
                    with col2:
                        st.markdown(f"""
                            <div class="weather-card">
                                <div>Day: {row['temp_day']}°C</div>
                                <div>Night: {row['temp_night']}°C</div>
                                <div>{row['weather'][0]['description'].capitalize()}</div>
                            </div>
                        """, unsafe_allow_html=True)

        except ValueError as e:
            st.error(f"⚠️ {str(e)}")
        except Exception as e:
            st.error(f"⚠️ Error: {str(e)}\nPlease try again later.")

except Exception as e:
    st.error("⚠️ Failed to initialize weather service. Please check if the API key is correctly set.")

# Footer
st.markdown("---")
st.markdown("Data provided by OpenWeather API")