import React from 'react';
import Navbar from './components/Navbar';
import WeatherCard from './components/WeatherCard';

function App() {
  return (
    <div className="bg-gray-100 h-screen">
      <Navbar />
      <main className="container mx-auto p-4">
        <WeatherCard />
      </main>
    </div>
  );
}

export default App;