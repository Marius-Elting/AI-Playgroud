/* eslint-disable @typescript-eslint/no-explicit-any */
"use client"
import React, { useState, useEffect } from 'react';
import axios from "axios";



interface Message {
    content: string;
    role: 'user' | 'assistant';
}
let gumStream: any = null;
let recorder: any = null;
let audioContext: any = null;

const Chat = () => {
    const [userInput, setUserInput] = useState('');
    const [imageInput, setImageInput] = useState<File | null>(null);
    const [output, setOutput] = useState<Message[]>([]);
    const [chunks, setChunks] = useState<any[]>([]);
    const [recorderState, setRecorderState] = useState(null);

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

    const startRecording = () => {
        let constraints = {
            audio: true,
            video: false
        }

        audioContext = new window.AudioContext();
        console.log("sample rate: " + audioContext.sampleRate);

        navigator.mediaDevices
            .getUserMedia(constraints)
            .then(function (stream) {
                console.log("initializing Recorder.js ...");

                gumStream = stream;

                const input: any = audioContext.createMediaStreamSource(stream);

                recorder = new window.MediaRecorder(stream, {
                    mimeType: 'audio/webm'
                })
                setRecorderState(recorder);
                recorder.start();
                console.log(recorder.state)

                console.log("Recording started");
            }).catch(function (err) {
                console.log("error: " + err);
                //enable the record button if getUserMedia() fails
        });

    }



    // ...
    const stopRecording = () => {
        console.log("stopButton clicked");
        if(recorderState == null) return;
        recorderState.stop()
        recorder.ondataavailable = (e) => {
            console.log("data available", e.data);
            const blob = e.data
            const audioOutput = document.querySelector('audio')!;
            audioOutput.src = window.URL.createObjectURL(blob);
            const data: any = new FormData();
            console.log(blob.type)
            data.append('audio', blob);
    
            const config = {
                headers: {'content-type': 'multipart/form-data'}
            }
            axios.post('http://localhost:8000/api/chat/upload_audio', data, config);
        };
    }

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
            <button onClick={handleSendMessage}>Send</button>
            <button onClick={startRecording} type="button">Start</button>
            <button onClick={stopRecording} type="button">Stop</button>
            <audio controls>
                <source src="audio.ogg" type="audio/mp3" />
                Your browser does not support the audio element.
            </audio>
        </div>
    );
};

export default Chat;