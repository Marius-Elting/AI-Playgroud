"use client"
import React, { useState } from 'react';

interface Message {
    content: string;
    role: 'user' | 'assistant';
}

const Chat = () => {
    const [userInput, setUserInput] = useState('');
    const [imageInput, setImageInput] = useState<File | null>(null);
    const [output, setOutput] = useState<Message[]>([]);

    const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        setUserInput(event.target.value);
    };

    const handleImageChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        if (event.target.files && event.target.files.length > 0) {
            setImageInput(event.target.files[0]);
        }
    };

    const handleSendClick = async () => {
        const userMessage: Message = {
            content: userInput,
            role: 'user',
        };

        setOutput((prevOutput) => [...prevOutput, userMessage]);
        setUserInput('');

        if (imageInput) {
            const formData = new FormData();
            formData.append('image', imageInput);
            formData.append('message', userInput);

            try {
                const response = await fetch('http://localhost:8000/api/chat/ask_image', {
                    method: 'POST',
                    body: formData,
                });
                if(!response.ok|| !response.body) throw new Error('Network response was not ok');
                const reader = response.body.getReader();
                const decoder = new TextDecoder();

                let result = '';
                let done = false;
                const assistantMessage: Message = {
                    content: '',
                    role: 'assistant',
                };
                setOutput((prevOutput) => [...prevOutput, assistantMessage]);
                
                while (!done) {
                    const { value, done: readerDone } = await reader.read();
                    const chunk = decoder.decode(value);
                    result += chunk;
                    setOutput((prevOutput) => {
                        const updatedOutput = [...prevOutput];
                        const lastMessageIndex = updatedOutput.length - 1;
                        updatedOutput[lastMessageIndex] = { content: result, role: 'assistant' };
                        return updatedOutput;
                    });

                    if (readerDone) {
                        done = true;
                    }
                }

                const data = JSON.parse(result);
                console.log(data)

                // Handle the response as needed
            } catch (error) {
                console.error(error);
                // Handle the error
            }
        }
    };

    return (
        <div>
            <div>
                Output:
                {output.map((message, index) => (
                    <div key={index}>
                        {message.role === 'user' ? 'User: ' : 'Assistant: '}
                        {message.content}
                    </div>
                ))}
            </div>
            <input type="text" value={userInput} onChange={handleInputChange} />
            <input type="file" onChange={handleImageChange} />
            <button onClick={handleSendClick}>Send</button>
        </div>
    );
};

export default Chat;