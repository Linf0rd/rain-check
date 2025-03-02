# Rain Check

Rain Check is a web application that provides weather information for a given city.

## Features

*   Displays current weather conditions for a city
*   Provides hourly and daily weather forecasts
*   Allows users to search for weather information for different cities
*   Caches weather data to reduce API calls
*   Stores user search history in a database

## Technologies Used

*   Python
*   Streamlit
*   SQLAlchemy
*   Requests
*   Plotly

## Installation

1.  Clone the repository:

    ```
    git clone https://github.com/Linf0rd/rain-check.git
    ```
2.  Install the required packages:

    ```
    pip install .
    ```
3.  Set the environment variables:

    *   `OPENWEATHER_API_KEY`: Your OpenWeather API key
    *   `DATABASE_URL`: The URL for your PostgreSQL database

4.  Run the app:

    ```
    streamlit run main.py
    ```

## Contributing

Contributions are welcome! Please submit a pull request with your changes.
