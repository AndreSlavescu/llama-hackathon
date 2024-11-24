import React from 'react';
import MessageBubble from './MessageBubble';

const ChatMessages = ({ userMessages, llmMessages }) => {
  userMessages = ["hi whats up", "ok bye"];
  llmMessages = ["Nothing, u?", "bye"];
  const messages = [];
  const maxLength = Math.max(userMessages.length, llmMessages.length);

  for (let i = 0; i < maxLength; i++) {
    if (i < userMessages.length) {
      messages.push({ text: userMessages[i], isLLM: false });
    }
    if (i < llmMessages.length) {
      messages.push({ text: llmMessages[i], isLLM: true });
    }
  }

  return (
    <div className="flex flex-col space-y-4 p-4">
      {messages.map((message, index) => (
        <MessageBubble key={index} text={message.text} isLLM={message.isLLM} />
      ))}
    </div>
  );
};

export default ChatMessages;