# Weather Forecast Application

A responsive weather forecast web application built with Streamlit, providing comprehensive weather information with interactive features.

## Features
- Current weather conditions
- Hourly forecast (24 hours)
- 7-day forecast
- Historical weather data (30 days)
- City search with suggestions
- Temperature, humidity, wind speed, and pressure
- Interactive charts and visualizations

## Tech Stack
- Streamlit
- OpenWeather API
- Python
- Pandas for data manipulation
- Plotly for visualizations
- PostgreSQL for data storage

## Setup Instructions

1. Clone the repository:
```bash
git clone <your-repository-url>
```

2. Install dependencies:
```bash
pip install streamlit pandas plotly psycopg2-binary sqlalchemy requests
```

3. Set up environment variables:
   - Create a `.env` file in the root directory
   - Add your OpenWeather API key:
     ```
     OPENWEATHER_API_KEY=your_api_key_here
     ```

4. Run the application:
```bash
streamlit run main.py
```

## Database Setup
The application uses PostgreSQL for storing search history and weather data cache. Make sure to set up your database connection string in the environment variables:
```
DATABASE_URL=postgresql://username:password@host:port/database
```

## Project Structure
```
├── .streamlit/          # Streamlit configuration
├── database.py          # Database models and connection
├── main.py             # Main application file
├── styles.py           # Custom CSS styles
├── visualization.py    # Data visualization components
├── weather_service.py  # Weather API service
└── README.md          # Project documentation
```

## Contributing
Feel free to submit issues and pull requests.

## License
This project is open source and available under the MIT License.