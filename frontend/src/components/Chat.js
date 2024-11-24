import React, { useState } from 'react';
import ChatBar from "./ChatBar";
import ChatMessages from "./ChatMessages";

const Chat = (props) => {
    const [userMessages, setUserMessages] = useState([]);
    const [llmMessages, setLlmMessages] = useState(["Hi, how can I help you today?"]);

    const handlerUserMessage = (userMessage) => {
        console.log("mesg", userMessage);
        setUserMessages((prevMessages) => [...prevMessages, userMessage]);
        console.log("hehe", userMessages);
    };

    return (
        <div className="flex flex-col h-full">
            <div className="flex-1 overflow-y-auto mb-16">
                <ChatMessages userMessages={userMessages} llmMessages={llmMessages} />
            </div>
            <div className="absolute bottom-0 left-0 right-0 p-4 bg-white">
                <ChatBar searchFunction={handlerUserMessage} />
            </div>
        </div>
    );
};

export default Chat;