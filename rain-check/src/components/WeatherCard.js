import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { FaSearch, FaSun, FaMoon, FaWind } from 'react-icons/fa'; // For icons

const WeatherCard = () => {
  const [weather, setWeather] = useState(null);
  const [city, setCity] = useState('');
  const [location, setLocation] = useState('Johannesburg'); // Default city
  const [darkMode, setDarkMode] = useState(false);
  const [errorMessage, setErrorMessage] = useState(null);

  // Define fetchWeather function at the top level
  const fetchWeather = async (lat, lon, cityName) => {
    try {
      const response = await axios.get(
        `https://api.open-meteo.com/v1/forecast?latitude=${lat}&longitude=${lon}&current_weather=true`
      );
      setWeather({ ...response.data.current_weather, cityName });
    } catch (error) {
      setErrorMessage('Error fetching weather data');
      console.error("Error fetching weather data:", error);
    }
  };

  useEffect(() => {
    // Geolocation or Default City Weather Fetch
    if (navigator.geolocation && !city) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          const { latitude, longitude } = position.coords;
          fetchWeather(latitude, longitude, 'Your Location');
        },
        () => {
          fetchWeather(-26.2041, 28.0473, 'Johannesburg'); // Default to Johannesburg
        }
      );
    } else {
      fetchWeather(-26.2041, 28.0473, location); // Default to Johannesburg
    }
  }, [location]); // 'location' is included in the dependency array

  const handleSearch = async (e) => {
    e.preventDefault();
    if (!city) return;

    // Use Nominatim API to convert city name to coordinates
    try {
      const geoResponse = await axios.get(
        `https://nominatim.openstreetmap.org/search?city=${city}&format=json`
      );
      const { lat, lon } = geoResponse.data[0];
      setLocation(city);
      setCity(''); // Reset the search bar
      fetchWeather(lat, lon, city); // Fetch weather for searched city
    } catch (error) {
      setErrorMessage('City not found. Please try again.');
    }
  };

  const toggleDarkMode = () => {
    setDarkMode(!darkMode);
  };

  if (!weather && !errorMessage) return <div>Loading...</div>;

  return (
    <div className={`${darkMode ? 'bg-gray-900 text-white' : 'bg-gray-100 text-black'} h-screen p-6`}>
      <div className="container mx-auto">
        {/* Search Bar */}
        <form onSubmit={handleSearch} className="flex mb-4">
          <input
            type="text"
            value={city}
            onChange={(e) => setCity(e.target.value)}
            placeholder="Search for a city..."
            className="p-2 rounded-l bg-white text-black w-full"
          />
          <button type="submit" className="bg-blue-500 text-white p-2 rounded-r">
            <FaSearch />
          </button>
        </form>

        {/* Dark/Light Toggle Button */}
        <button onClick={toggleDarkMode} className="mb-4 p-2 bg-gray-700 text-white rounded">
          {darkMode ? <FaSun /> : <FaMoon />} Toggle {darkMode ? 'Light' : 'Dark'} Mode
        </button>

        {/* Weather Display */}
        {errorMessage && <p className="text-red-500">{errorMessage}</p>}
        {weather && (
          <div className="bg-white shadow-lg p-6 rounded-lg">
            <h2 className="text-2xl font-bold">{weather.cityName}</h2>
            <p className="text-xl">
              <FaWind /> Wind: {weather.windspeed} km/h
            </p>
            <p className="text-xl">
              <FaSun /> Temperature: {weather.temperature}°C
            </p>
          </div>
        )}
      </div>
    </div>
  );
};

export default WeatherCard;