import React, { useState } from 'react';
import logo from './logo.svg';
import 'leaflet/dist/leaflet.css';
import './App.css';
import SearchBar from './components/SearchBar';
import "./leaflet"
import LLMContainer from './components/LLMContainer';

function App() {
  const [query, setQuery]= useState("")
  const searchFunction = (query) => {
    console.log("Querying", query)
    setQuery(query.trim())

  }
  return (
    <div className="App">
      {!query? <SearchBar searchFunction={searchFunction}/> : <LLMContainer />}

      
    </div>
  );
}

export default App;
