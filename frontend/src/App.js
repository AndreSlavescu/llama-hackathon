import React, { useState } from 'react';
import 'leaflet/dist/leaflet.css';
import './App.css';
import { Search } from 'lucide-react';
import "./leaflet";
import LLMContainer from './components/LLMContainer';
import logo from "./styles/nest_quest.png"

const BackgroundPattern = () => {
  const shapes = [
    { size: 'w-64 h-64', color: 'bg-blue-500/10', duration: '20s', delay: '0s' },
    { size: 'w-96 h-96', color: 'bg-purple-500/10', duration: '25s', delay: '2s' },
    { size: 'w-72 h-72', color: 'bg-cyan-500/10', duration: '22s', delay: '4s' },
    { size: 'w-80 h-80', color: 'bg-indigo-500/10', duration: '28s', delay: '1s' },
    { size: 'w-48 h-48', color: 'bg-sky-500/10', duration: '18s', delay: '3s' },
    { size: 'w-56 h-56', color: 'bg-blue-400/10', duration: '23s', delay: '5s' },
  ];

  return (
    <div className="fixed inset-0 -z-10 overflow-hidden">
      <div className="absolute inset-0 bg-gradient-to-b from-slate-900 via-slate-800 to-slate-900" />
      
      <div className="absolute inset-0">
        {shapes.map((shape, i) => (
          <div
            key={i}
            className={`
              absolute rounded-full ${shape.size} ${shape.color}
              backdrop-blur-3xl animate-float
            `}
            style={{
              animation: `
                float ${shape.duration} ease-in-out infinite,
                moveAround ${parseInt(shape.duration) * 1.5}s ease-in-out infinite
              `,
              animationDelay: shape.delay,
              filter: 'blur(50px)',
              left: '50%',
              top: '50%',
              transform: 'translate(-50%, -50%)'
            }}
          />
        ))}
      </div>

      <div className="absolute inset-0 bg-gradient-to-r from-transparent via-blue-500/5 to-transparent animate-pulse-slow" />
    </div>
  );
};

const SearchInterface = ({ onSearch }) => {
  const [query, setQuery] = useState('');
  const [isFocused, setIsFocused] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (query.trim()) {
      onSearch(query);
    }
  };

  return (
    <div className="min-h-screen flex flex-col px-4 bg-gradient-to-r from-blue-500 to-indigo-600">
      <div className="absolute top-6 left-8">
        <img
          src={logo}
          alt="Nest Logo"
          className="w-100 h-24 pointer-events-none"
        />
      </div>

      <div className="flex-1 flex items-center justify-center">
        <div className="w-full max-w-3xl">
          <div className="text-center">
            <h2 className="text-5xl font-bold text-white leading-tight mb-0">
              Your Perfect Home Awaits Discovery
            </h2>
          </div>

          <form onSubmit={handleSubmit} className="relative mt-8">
            <div
              className={`relative transition-all duration-300 transform ${
                isFocused ? 'scale-105' : 'scale-100'
              }`}
            >
              <div className="absolute inset-y-0 left-4 flex items-center pointer-events-none">
                <Search
                  className={`w-5 h-5 transition-colors duration-200 ${
                    isFocused ? 'text-blue-500' : 'text-slate-400'
                  }`}
                />
              </div>
              <input
                type="text"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                onFocus={() => setIsFocused(true)}
                onBlur={() => setIsFocused(false)}
                placeholder="Where would you like to live?"
                className="w-full px-12 py-4 bg-white rounded-full shadow-lg text-lg focus:outline-none focus:ring-2 focus:ring-blue-500 transition-shadow duration-200"
              />
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

function App() {
  const [query, setQuery] = useState("");
  
  const searchFunction = (query) => {
    console.log("Querying", query);
    setQuery(query.trim());
  };

  return (
    <div className="App relative">
      {!query ? <SearchInterface onSearch={searchFunction} /> : <LLMContainer />}
    </div>
  );
}

export default App;