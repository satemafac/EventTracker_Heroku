import React, { useState, useEffect, useRef } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faMicrophone, faMicrophoneSlash } from '@fortawesome/free-solid-svg-icons';

function MicrophoneComponent() {
    const [recording, setRecording] = useState(false);
    const [mediaRecorder, setMediaRecorder] = useState(null);
    const [transcription, setTranscription] = useState("");
    const socketRef = useRef(null);

    useEffect(() => {
        socketRef.current = new WebSocket('ws://127.0.0.1:8001/ws/transcribe/');
        
        socketRef.current.onopen = (event) => {
            console.log("WebSocket is open now.");
        };

        socketRef.current.onmessage = (event) => {
            const data = JSON.parse(event.data);
            console.log(data.transcription);
            setTranscription(data.transcription);
        };

        return () => {
            if (socketRef.current && socketRef.current.readyState === WebSocket.OPEN) {
                socketRef.current.close();
            }
        };
    }, []);

    const handleMicrophoneClick = async () => {
        if (!recording) {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            
            const newMediaRecorder = new MediaRecorder(stream);
            
            console.log("Using MIME type:", newMediaRecorder.mimeType);
            
            let accumulatedChunks = [];

            newMediaRecorder.ondataavailable = async (event) => {
                accumulatedChunks.push(event.data);
                
                const blob = new Blob(accumulatedChunks, { type: 'audio/webm' });
                const arrayBuffer = await blob.arrayBuffer();
                socketRef.current.send(arrayBuffer);
            };

            newMediaRecorder.onstart = () => {
                accumulatedChunks = [];
                setRecording(true);
            };

            newMediaRecorder.onstop = () => {
                setRecording(false);
                const tracks = stream.getTracks();
                tracks.forEach(track => track.stop());
            };

            newMediaRecorder.start(4000);
            setMediaRecorder(newMediaRecorder);
        } else if (mediaRecorder) {
            mediaRecorder.stop();
        }
    };

    return (
        <div style={{ height: '100vh', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center' }}>
            <div 
                onClick={handleMicrophoneClick}
                style={{ 
                    width: '50px', 
                    height: '50px', 
                    borderRadius: '50%', 
                    backgroundColor: recording ? '#99cfe0' : 'gray', 
                    display: 'flex', 
                    alignItems: 'center', 
                    justifyContent: 'center', 
                    cursor: 'pointer',
                    transition: 'background-color 0.3s'
                }}
                onMouseOver={(e) => e.currentTarget.style.backgroundColor = recording ? '#5eb3ce' : 'darkgray'}
                onMouseOut={(e) => e.currentTarget.style.backgroundColor = recording ? '#99cfe0' : 'gray'}
            >
                <FontAwesomeIcon 
                    icon={recording ? faMicrophone : faMicrophoneSlash} 
                    size="2x"
                />
            </div>
            <div style={{ marginTop: '20px', fontSize: '18px' }}>
                {transcription}
            </div>
        </div>
    );
}

export default MicrophoneComponent;
