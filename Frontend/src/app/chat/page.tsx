/* eslint-disable @typescript-eslint/no-explicit-any */
"use client"
import React, { useState } from 'react';
import styles from "./page.module.scss";


interface Message {
    content: string;
    role: 'user' | 'assistant';
    type: 'text' | 'image' | 'audio';
    audioFile?: any;
}

const Chat = () => {
    const [userInput, setUserInput] = useState('');
    const [imageInput, setImageInput] = useState<File | null>(null);
    const [history, setHistory] = useState<Message[]>([]);
    const [recorderState, setRecorderState] = useState<MediaRecorder>();
    const [loading, setLoading] = useState(false);

    const downloadFile = async () => {
        setLoading(true);
        try {
            const data = new FormData();
            data.append('history', JSON.stringify(history));
            const response = await fetch('http://127.0.0.1:8000/api/chat/get_excel', {
                "method": "POST",
                "body": data,         
            });
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'output.xlsx';
            document.body.appendChild(a);
            a.click();
            a.remove();
        } catch (error) {
            console.error('Error downloading the file:', error);
        } finally {
            setLoading(false);
        }
    }
    const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        setUserInput(event.target.value);
    };

    const handleImageChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        if (event.target.files && event.target.files.length > 0) {
            setImageInput(event.target.files[0]);
        }
    };

    const handleSendMessage = async () => {
        const userMessage: Message = {
            content: userInput,
            role: 'user',
            type: imageInput ? 'image' : 'text',
        };

        setHistory((prevHistory) => [...prevHistory, userMessage]);
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
                if (!response.ok || !response.body) throw new Error('Network response was not ok');
                const reader = response.body.getReader();
                const decoder = new TextDecoder();

                let result = '';
                let done = false;
                const assistantMessage: Message = {
                    content: '',
                    role: 'assistant',
                    type: 'text',
                };
                setHistory((prevHistory) => [...prevHistory, assistantMessage]);

                while (!done) {
                    const { value, done: readerDone } = await reader.read();
                    const chunk = decoder.decode(value);
                    result += chunk;
                    setHistory((prevHistory) => {
                        const updatedHistory = [...prevHistory];
                        const lastMessageIndex = updatedHistory.length - 1;
                        updatedHistory[lastMessageIndex] = { content: result, role: 'assistant', type: "text" };
                        return updatedHistory;
                    });

                    if (readerDone) {
                        done = true;
                    }
                }


            } catch (error) {
                console.error(error);
            }
        } else {
            const formData = new FormData()
            formData.append('question', userInput)
            const response = await fetch('http://localhost:8000/api/chat/ask', {
                method: 'POST',
                body: formData,
            });
            if (!response.ok || !response.body) throw new Error('Network response was not ok');
            const reader = response.body.getReader();
            const decoder = new TextDecoder();

            let result = '';
            let done = false;
            const assistantMessage: Message = {
                content: '',
                role: 'assistant',
                type: 'text',
            };
            setHistory((prevHistory) => [...prevHistory, assistantMessage]);

            while (!done) {
                const { value, done: readerDone } = await reader.read();
                const chunk = decoder.decode(value);
                result += chunk;
                setHistory((prevHistory) => {
                    const updatedHistory = [...prevHistory];
                    const lastMessageIndex = updatedHistory.length - 1;
                    updatedHistory[lastMessageIndex] = { content: result, role: 'assistant', type: "text" };
                    return updatedHistory;
                });

                if (readerDone) {
                    done = true;
                }
            }
        }
    };

    const startRecording = () => {
        const constraints = {
            audio: true,
            video: false
        }

        navigator.mediaDevices
            .getUserMedia(constraints)
            .then(function (stream) {
                console.log("initializing Recorder.js ...");

                const recorder = new window.MediaRecorder(stream, {
                    mimeType: 'audio/webm'
                })
                setRecorderState(recorder);
                recorder.start();
                console.log(recorder.state)

                console.log("Recording started");
            }).catch(function (err) {
                console.log("error: " + err);
            });
    }

    const stopRecording = async () => {
        console.log("stopButton clicked");
        if (recorderState == null) return;
        recorderState.stop()

        recorderState.ondataavailable = async (e) => {
            console.log("data available", e.data);
            const blob = e.data
            /*  const audioHistory = document.querySelector('audio')!;
             audioHistory.src = window.URL.createObjectURL(blob); */
            const data: any = new FormData();
            console.log(blob.type)
            data.append('audio', blob);
            const userMessage: Message = {
                content: '',
                role: 'user',
                type: 'audio',
                audioFile: window.URL.createObjectURL(blob),
            };
            setHistory((prevHistory) => [...prevHistory, userMessage]);

            const response = await fetch('http://localhost:8000/api/chat/upload_audio', {
                method: 'POST',
                body: data,
            });

            if (!response.ok || !response.body) throw new Error('Network response was not ok');
            const reader = response.body.getReader();
            const decoder = new TextDecoder();

            let result = '';
            let done = false;
            const assistantMessage: Message = {
                content: '',
                role: 'assistant',
                type: 'text',
            };
            setHistory((prevHistory) => [...prevHistory, assistantMessage]);

            while (!done) {
                const { value, done: readerDone } = await reader.read();
                const chunk = decoder.decode(value);
                result += chunk;
                setHistory((prevHistory) => {
                    const updatedHistory = [...prevHistory];
                    const lastMessageIndex = updatedHistory.length - 1;
                    updatedHistory[lastMessageIndex] = { content: result, role: 'assistant', type: "text" };
                    return updatedHistory;
                });

                if (readerDone) {
                    done = true;
                }
            }
        };
    }

    return (
        <div className={styles.chat_wrapper}>
            <div className={styles.chat_output}>
                {history.map((message, index) => (
                    message.type == "text" ? (
                        <div key={index} className={message.role == "user" ? styles.user_message : styles.assistant_message}>
                            {message.content}
                        </div>
                    ) : (message.type == "image") ? (

                        <div key={index} className={message.role == "user" ? styles.user_message : styles.assistant_message}>
                            {/*  <img src={URL.createObjectURL(imageInput)} alt="user_image" /> */}
                            {message.content}
                        </div>
                    ) : (
                        <div key={index} className={message.role == "user" ? styles.user_message : styles.assistant_message}>
                            <audio controls>
                                <source src={message.audioFile} type="audio/mp3" />
                                Your browser does not support the audio element.
                            </audio>
                        </div>
                    )
                ))}
            </div>
            <div className={styles.chat_input}>

                <input type="text" value={userInput} onChange={handleInputChange} />

                <label htmlFor="fileInput">Upload</label>
                <input type="file" id="fileInput" onChange={handleImageChange} />
                <button onClick={handleSendMessage}>Send</button>
                <div>
                    <button onClick={startRecording} type="button">Start</button>
                    <button onClick={stopRecording} type="button">Stop</button>
                </div>
                <button onClick={downloadFile} type="button" disabled={loading}>download excel</button>
                {/* <audio controls>
                    <source src="audio.ogg" type="audio/mp3" />
                    Your browser does not support the audio element.
                </audio> */}
            </div>

        </div>
    );
};

export default Chat;