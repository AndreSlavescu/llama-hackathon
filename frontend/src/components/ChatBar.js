import React, { useRef } from 'react';

const ChatBar = (props) => {
  const searchRef = useRef();
  
  const searchHandler = () => {
    const query = searchRef.current.value;
    props.searchFunction(query);
    searchRef.current.value = "";
  };

  const handlerEnter = (event) => {
    if (event.key === 'Enter') {
      searchHandler();
    }
  };

  return (
    <div className="relative w-full">
      <input
        type="text"
        className="w-full px-12 py-3 bg-gray-100 rounded-full focus:outline-none focus:ring-2 focus:ring-blue-500 focus:bg-white transition-all"
        placeholder="Ask follow-up"
        ref={searchRef}
        onKeyDown={handlerEnter}
      />
      <svg 
        className="absolute left-4 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400"
        xmlns="http://www.w3.org/2000/svg"
        height="24px"
        width="24px"
        fill="currentColor"
        viewBox="0 0 24 24"
      >
        <path d="M15.5 14h-.79l-.28-.27A6.471 6.471 0 0016 9.5 6.5 6.5 0 109.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C8 14 6 12 6 9.5S8 5 9.5 5 13 7 13 9.5 11 14 9.5 14z"/>
      </svg>
    </div>
  );
};

export default ChatBar;