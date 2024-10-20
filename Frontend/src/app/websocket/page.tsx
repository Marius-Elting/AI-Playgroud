"use client"
import React, { useState, useEffect } from 'react';
import styles from './page.module.scss';

const WebSocketComponent: React.FC = () => {
  const [inputValue, setInputValue] = useState<string>('');
  const [messages, setMessages] = useState<string[]>([]);
  const [ws, setWs] = useState<WebSocket | null>(null);

  useEffect(() => {
    const socket = new WebSocket('ws://localhost:8000/ws');
    setWs(socket);

    socket.onmessage = (event) => {
      setMessages((prevMessages) => [...prevMessages, event.data]);
    };

    return () => {
      socket.close();
    };
  }, []);

  const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setInputValue(event.target.value);
  };

  const handleSendMessage = () => {
    if (ws && inputValue) {
      ws.send(inputValue);
      setInputValue('');
    }
  };

  return (
    <div className={styles.webSocketComponent}>
      <input
        type="text"
        value={inputValue}
        onChange={handleInputChange}
        placeholder="Enter message"
        className={styles.inputField}
      />
      <button onClick={handleSendMessage} className={styles.sendButton}>
        Send
      </button>
      <div className={styles.messages}>
        {messages.map((message, index) => (
          <div key={index} className={styles.message}>
            {message}
          </div>
        ))}
      </div>
    </div>
  );
};

export default WebSocketComponent;