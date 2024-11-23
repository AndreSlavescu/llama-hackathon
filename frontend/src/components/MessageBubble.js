import React from 'react';

const MessageBubble = ({ text, isLLM }) => {
  const bubbleStyle = {
    maxWidth: '60%',
    padding: '10px 15px',
    borderRadius: '20px',
    margin: '5px 0',
    alignSelf: isLLM ? 'flex-start' : 'flex-end',
    backgroundColor: isLLM ? '#d4edda' : '#e1ffc7',
    color: '#000',
    wordWrap: 'break-word',
    boxShadow: '0 1px 3px rgba(0,0,0,0.1)',
  };
  
  const containerStyle = {
    display: 'flex',
    flexDirection: 'column',
    alignItems: isLLM ? 'flex-start' : 'flex-end',
  };
  
  return (
    <div style={containerStyle}>
      <div style={bubbleStyle}>
        {text}
      </div>
    </div>
  );
};

export default MessageBubble;
