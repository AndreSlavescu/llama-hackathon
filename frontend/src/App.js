import React, { useState } from 'react';
import 'leaflet/dist/leaflet.css';
import './App.css';
import { Search } from 'lucide-react';
import "./leaflet";
import LLMContainer from './components/LLMContainer';

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
    <div className="min-h-screen bg-gradient-to-b from-slate-900 to-slate-800 flex items-center justify-center px-4">
      <div className="w-full max-w-3xl">
        {/* Hero Section */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-white mb-4">
            Discover Knowledge
          </h1>
          <p className="text-slate-300 text-lg">
            What would you like to learn about today?
          </p>
        </div>

        {/* Search Form */}
        <form onSubmit={handleSubmit} className="relative">
          <div className={`relative transition-all duration-300 transform ${
            isFocused ? 'scale-105' : 'scale-100'
          }`}>
            <div className="absolute inset-y-0 left-4 flex items-center pointer-events-none">
              <Search className={`w-5 h-5 transition-colors duration-200 ${
                isFocused ? 'text-blue-500' : 'text-slate-400'
              }`} />
            </div>
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              onFocus={() => setIsFocused(true)}
              onBlur={() => setIsFocused(false)}
              placeholder="Type your question here..."
              className="w-full px-12 py-4 bg-white rounded-full shadow-lg text-lg focus:outline-none focus:ring-2 focus:ring-blue-500 transition-shadow duration-200"
            />
          </div>
        </form>

        {/* Feature Pills */}
        <div className="mt-8 flex flex-wrap justify-center gap-2">
          {['Quick Answers', 'Deep Learning', 'Real-time Updates'].map((feature) => (
            <div
              key={feature}
              className="px-4 py-2 bg-slate-700/50 rounded-full text-slate-300 text-sm"
            >
              {feature}
            </div>
          ))}
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
    <div className="App">
      {!query ? <SearchInterface onSearch={searchFunction} /> : <LLMContainer />}
    </div>
  );
}

export default App;
