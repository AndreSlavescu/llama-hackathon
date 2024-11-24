import React, { useState } from 'react'
import ChatBar from "./ChatBar"
import ChatMessages from "./ChatMessages"


const Chat = (props) => {
    const [userMessages, setUserMessages] = useState([])
    const [llmMessages, setLlmMessages] = useState([])

    const handlerUserMessage = (userMessage) => {
        console.log("mesg", userMessage)
        setUserMessages((prevMessages) => [...prevMessages, userMessage]);
        console.log("hehe", userMessages)

    }

  return (
    <div>
        <ChatMessages userMessages={userMessages} llmMessages={llmMessages}/>
        <ChatBar searchFunction={handlerUserMessage}/>
    </div>
  )
}



export default Chat


