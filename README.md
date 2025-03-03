# Rain Check

![image](https://github.com/user-attachments/assets/8c6149f1-08b8-44ca-9cbc-e29a21df9ec6)

Rain Check is a web application that provides weather information for a given city. It allows users to search for weather forecasts and view current weather conditions, hourly forecasts, and a detailed daily forecast.

## Features

*   **Current Weather Conditions:** Displays real-time weather data for a specified city, including temperature, conditions, humidity, and wind speed.
*   **Hourly Forecast:** Provides an hourly temperature forecast for the next 24 hours.
*   **Detailed Daily Forecast:** Shows a 7-day forecast, including high and low temperatures and weather conditions for each day.
*   **City Search:** Allows users to search for weather information for any city in the world.
*   **Popular City Suggestions:** Provides a list of popular cities for quick selection.
*   **Data Caching:** Caches weather data to reduce API calls and improve performance.
*   **Search History:** Stores user search history in a database for future reference.

## Technologies Used

*   **Python:** The primary programming language used for the application.
*   **Streamlit:** A Python library used to create the web application interface.
*   **SQLAlchemy:** A Python SQL toolkit and Object-Relational Mapper (ORM) used to interact with the database.
*   **Requests:** A Python library used to make HTTP requests to the OpenWeather API.
*   **Plotly:** A Python library used to create interactive charts and graphs.
*   **OpenWeather API:** A weather API used to retrieve weather data.
*   **PostgreSQL:** A relational database used to store search history and cached weather data.
*   **python-dotenv:** Used to load environment variables from a .env file.

## Installation

1.  Clone the repository:

    ```bash
    git clone https://github.com/Linf0rd/rain-check.git
    ```

2.  Install the required packages:

    ```bash
    pip install .
    ```

3.  Set the environment variables:

    Create a `.env` file in the root directory of the project and add the following environment variables:

    ```
    OPENWEATHER_API_KEY="your_openweather_api_key"
    DATABASE_URL="your_postgresql_database_url"
    ```

    Replace `"your_openweather_api_key"` with your actual OpenWeather API key and `"your_postgresql_database_url"` with the URL for your PostgreSQL database.

4.  Run the app:

    ```bash
    streamlit run main.py
    ```

## Contributing

Contributions are welcome! Please submit a pull request with your changes.

## API

This project uses the OpenWeather API to retrieve weather data. You can sign up for a free API key at [https://openweathermap.org/api](https://openweathermap.org/api).

## Database Schema

The project uses a PostgreSQL database to store search history and cached weather data. The database schema consists of two tables:

*   **search_history:** Stores user search history.
    *   `id` (INTEGER, PRIMARY KEY)
    *   `city` (VARCHAR)
    *   `timestamp` (DATETIME)

*   **weather_cache:** Stores cached weather data.
    *   `id` (INTEGER, PRIMARY KEY)
    *   `city` (VARCHAR)
    *   `lat` (FLOAT)
    *   `lon` (FLOAT)
    *   `current_data` (JSON)
    *   `hourly_data` (JSON)
    *   `daily_data` (JSON)
    *   `timestamp` (DATETIME)
      


 



