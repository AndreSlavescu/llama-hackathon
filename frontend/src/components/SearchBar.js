import React, { useRef } from 'react';
import '../styles/SearchBar.css';

const SearchBar = (props) => {
  const searchRef = useRef()
  const searchHandler = () => {
    const query = searchRef.current.value;
    props.searchFunction(query);

  }

  const handlerEnter = (event) => {
    if (event.key === 'Enter') {
      searchHandler();
    }
  };

  return (
    <div className="search-bar-container">
      <svg className="search-icon" xmlns="http://www.w3.org/2000/svg" height="24px" width="24px" fill="#888" viewBox="0 0 24 24">
        <path d="M15.5 14h-.79l-.28-.27A6.471 6.471 0 0016 9.5 6.5 6.5 0 109.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C8 14 6 12 6 9.5S8 5 9.5 5 13 7 13 9.5 11 14 9.5 14z"/>
      </svg>
      <input
        type="text"
        className="search-input"
        placeholder="Ask anything..."
        ref={searchRef}
        onKeyDown={handlerEnter}
      />
    </div>
  );
}

export default SearchBar;
