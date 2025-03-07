import streamlit as st
import pandas as pd
from datetime import datetime
from weather_service import WeatherService
from visualization import create_hourly_temp_chart
from styles import apply_custom_styles, get_weather_icon

# Page configuration
st.set_page_config(
    page_title="Weather Forecast",
    page_icon="🌤️",
    layout="wide"
)

# Apply custom styles
apply_custom_styles()

hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
[data-testid="stToolbar"] {visibility: hidden !important;}
[data-testid="column"]:nth-child(4) .weather-card {
    margin-bottom: 30px; /* Adjust this value as needed */
}
</style>

"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

try:
    # Initialize weather service
    weather_service = WeatherService()

    # Header
    st.title("🌤 Rain Check")
    st.markdown("Get detailed weather forecasts for any location.")

    # Get list of popular cities for suggestions
    popular_cities = [
        "Johannesburg", "Cape Town", "Durban", "Pretoria", "Gqeberha (Port Elizabeth)", "Bloemfontein", "East London", "Kimberley", "Polokwane", "Mbombela (Nelspruit)", "Pietermaritzburg",
        "Rustenburg", "George", "Stellenbosch", "Worcester", "Upington", "Klerksdorp", "Newcastle", "Mthatha", "Vereeniging", "Vanderbijlpark", "Welkom", "Witbank (eMalahleni)",
        "Beaufort West", "Graaff-Reinet", "Oudtshoorn", "Swellendam", "Paarl", "Springbok", "Vryburg", "Bethlehem", "Harrismith", "Ladysmith", "Richards Bay", "Potchefstroom", "Kroonstad", "Queenstown(Komani)", "Mahikeng(Mafikeng)", "Phalaborwa",
        "London", "New York", "Tokyo", "Paris", "Sydney", "Dubai"
    ]

    # Search bar with autocomplete
    city = st.selectbox(
        "Enter city name",
        options=popular_cities,
        index=0,  # Set Johannesburg as default
        key="city_search"
    )

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
                col1, col2, col3, col4 = st.columns(4)

                with col1:
                    st.markdown(f"""
                        <div class="weather-card">
                            <i class="{get_weather_icon(current['weather'][0]['main'])} weather-icon"></i>
                            <div>‎ </div>
                            <div>‎ </div>
                            <div class="condition-text">{current['weather'][0]['description'].capitalize()}</div>
                        </div>
                    """, unsafe_allow_html=True)

                with col2:
                    st.markdown(f"""
                        <div class="weather-card">
                            <i class="fas fa-temperature-high weather-icon"></i>
                            <div class="temp-text">{round(current['main']['temp'])}°C</div>
                            <div class="condition-text">Temperature</div>
                        </div>
                    """, unsafe_allow_html=True)

                with col3:
                    # Convert wind speed from m/s to km/h (multiply by 3.6)
                    wind_speed_kmh = round(current['wind']['speed'] * 3.6)
                    st.markdown(f"""
                        <div class="weather-card">
                            <i class="fas fa-wind weather-icon"></i>
                            <div class="temp-text">{wind_speed_kmh} km/h</div>
                            <div class="condition-text">Wind Speed</div>
                        </div>
                    """, unsafe_allow_html=True)

                with col4:
                    now = datetime.now()
                    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
                    st.markdown(f"""
                        <div class="weather-card">
                            <div> </div>
                            <div class="temp-text">{dt_string}</div>
                            <div class="condition-text">Date & Time</div>
                        </div>
                    """, unsafe_allow_html=True)

                    st.markdown("""
                        <script>
                        function updateTime() {
                            var now = new Date();
                            var dt_string = now.toLocaleTimeString();
                            document.querySelector('.weather-card div').innerText = dt_string;
                        }
                        setInterval(updateTime, 1000);
                        </script>
                    """, unsafe_allow_html=True)

                # Additional weather info
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"""
                        <div class="weather-card">
                            <i class="fas fa-tint weather-icon"></i>
                            <div class="temp-text">{current['main']['humidity']}%</div>
                            <div class="condition-text">Humidity</div>
                        </div>
                    """, unsafe_allow_html=True)

                with col2:
                    st.markdown(f"""
                        <div class="weather-card">
                            <i class="fas fa-compress-arrows-alt weather-icon"></i>
                            <div class="temp-text">{current['main']['pressure']} hPa</div>
                            <div class="condition-text">Pressure</div>
                        </div>
                    """, unsafe_allow_html=True)

                # Hourly forecast
                st.subheader("Hourly Forecast")
                hourly_data = weather_service.process_hourly_forecast({"hourly": weather_data['hourly']})
                st.plotly_chart(create_hourly_temp_chart(hourly_data), use_container_width=True)

                # Daily forecast
                daily_data = weather_service.process_daily_forecast(weather_data['daily'])

                # Detailed daily forecast
                st.subheader("Detailed Daily Forecast")
                for _, row in daily_data.iterrows():
                    st.markdown(f"""
                        <div class="weather-card">
                            <div style="font-weight: bold">{row['day']}</div>
                            <i class="{get_weather_icon(row['weather'][0]['main'])} weather-icon"></i>
                            <div style="font-size: 1.2rem">
                                <span style="color: #FF4B4B">High: {row['temp_day']}°C</span> | 
                                <span style="color: #4B9FFF">Low: {row['temp_night']}°C</span>
                            </div>
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
