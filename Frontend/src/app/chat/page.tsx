"use client"
import React, { useState } from 'react';
import styles from "./page.module.scss";


interface IMessage {
    content: string;
    role: 'user' | 'assistant';
    type: 'text' | 'image' | 'audio';
    audioFile?: Blob;
    imageFile?: File;
}

const Chat = () => {
    const [userInput, setUserInput] = useState('');
    const [imageInput, setImageInput] = useState<File | null>(null);
    const [history, setHistory] = useState<IMessage[]>([]);
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


        setUserInput('');
        if (imageInput) {
            const userMessage: IMessage = {
                content: userInput,
                role: 'user',
                type:'image',
                imageFile: imageInput,
            };
            setHistory((prevHistory) => [...prevHistory, userMessage]);

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
                const assistantMessage: IMessage = {
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
            const userMessage: IMessage = {
                content: userInput,
                role: 'user',
                type: 'text',
            };
            setHistory((prevHistory) => [...prevHistory, userMessage]);
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
            const assistantMessage: IMessage = {
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
            const data: FormData = new FormData();
            console.log(blob.type)
            data.append('audio', blob);
            const userMessage: IMessage = {
                content: '',
                role: 'user',
                type: 'audio',
                audioFile: blob
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
            const assistantMessage: IMessage = {
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
                {history.map((message: IMessage, index: number) => (
                    message.type == "text" ? (
                        <div key={index} className={message.role == "user" ? styles.user_message : styles.assistant_message}>
                            {message.content}
                        </div>
                    ) : (message.type == "image") ? (

                        <div key={index} className={message.role == "user" ? styles.user_message : styles.assistant_message}>
                            {message.imageFile && <img src={URL.createObjectURL(message.imageFile)} alt="user_image" />}
                            {message.content}
                        </div>
                    ) : (
                        <div key={index} className={message.role == "user" ? styles.user_message : styles.assistant_message}>
                            {message.audioFile && <audio controls>
                                <source src={window.URL.createObjectURL(message.audioFile)} type="audio/mp3" />
                                Your browser does not support the audio element.
                            </audio>}
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