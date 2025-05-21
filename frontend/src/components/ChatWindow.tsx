// ChatWindow.tsx
import React, { useEffect, useState } from 'react';
import MessageBubble from './MessageBubble.tsx';
import FeedbackForm from './FeedbackForm.tsx';
import { fetchVersion, getConversationMessages, createConversation } from './api.ts';

type Props = {
    conversationId: string | null;
    setConversationId: (id: string) => void;
};

export default function ChatWindow({ conversationId, setConversationId }: Props) {
    const [clearFeedbackFlags, setClearFeedbackFlags] = useState<boolean>(false);
    const [messages, setMessages] = useState<
        { sender: 'user' | 'bot'; text: string; version?: string; showFeedback?: boolean }[]
    >([]);
    const [input, setInput] = useState('');
    const [version, setVersion] = useState<string | null>(null);
    const [searchWebMode, setSearchWebMode] = useState(false);
    const [hasUploadedFile, setHasUploadedFile] = useState(false);


    useEffect(() => {
        const initialize = async () => {
            setVersion(null);

            if (!conversationId) {
                const newId = await createConversation();
                setConversationId(newId);
                await loadConversation(newId);
            } else {
                await loadConversation(conversationId);
            }
        };
        initialize();
    }, [conversationId]);

    const loadConversation = async (id: string) => {

        console.log(id);
        const fetched = await fetchVersion(id);
        setVersion(fetched);

        const history = await getConversationMessages(id);
        const formatted = history.map((msg: any) => ({
            sender: msg.role === 'assistant' ? 'bot' : 'user',
            text: msg.content,
            showFeedback: msg.role === 'assistant',
        }));
        setMessages(formatted);
    };

    const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
        const file = e.target.files?.[0];
        if (!file || !conversationId) return;

        const formData = new FormData();
        formData.append("file", file);

        try {
            const res = await fetch(`http://localhost:8000/api/v1/upload?conversation_id=${conversationId}`, {
                method: "POST",
                body: formData,

            });

            const data = await res.json();
            if (res.ok) {
                alert(`File uploaded successfully: ${data.filename}`);
                setHasUploadedFile(true);
            } else {
                alert(`Upload failed: ${data.detail}`);
            }
        } catch (err) {
            alert("Error uploading file");
        }
    };


    const handleWebSearch = () => {
        setSearchWebMode(prev => !prev);
    };


    const handleSend = async () => {

        if (!input.trim()) return;
        setClearFeedbackFlags(true);
        const userText = input;
        setInput('');

        const updatedMessages = messages.map((m) =>
            m.sender === 'bot' ? { ...m, showFeedback: false } : m
        );

        setMessages([...updatedMessages, { sender: 'user', text: userText }]);
        setMessages((prev) => [...prev, { sender: 'bot', text: '', showFeedback: false }]);


        let endpoint = `http://localhost:8000/api/v1/chatbot/stream?convo_id=${conversationId}&message=${encodeURIComponent(userText)}`;
        if (searchWebMode) {
            endpoint = `http://localhost:8000/api/v1/chatbot/web?convo_id=${conversationId}&message=${encodeURIComponent(userText)}`;
        } else if (hasUploadedFile) {
            endpoint = `http://localhost:8000/api/v1/chatbot/file?convo_id=${conversationId}&message=${encodeURIComponent(userText)}`;
            setHasUploadedFile(false);
        }

        const eventSource = new EventSource(endpoint);

        let fullReply = '';

        eventSource.onmessage = (event) => {
            const token = event.data;
            fullReply += token;
            setMessages((prev) => {
                const newMsgs = [...prev];
                const last = newMsgs[newMsgs.length - 1];
                newMsgs[newMsgs.length - 1] = { ...last, text: last.text + token };
                return newMsgs;
            });
        };

        eventSource.onerror = () => {
            eventSource.close();
            setMessages((prev) => {
                const newMsgs = [...prev];
                const last = newMsgs[newMsgs.length - 1];
                newMsgs[newMsgs.length - 1] = { ...last, showFeedback: true, version };
                return newMsgs;
            });
            if (window.dispatchEvent) {
                window.dispatchEvent(new Event("conversationUpdated"));
            }
        };

        eventSource.addEventListener('end', () => {
            setMessages((prev) => {
                const newMsgs = [...prev];
                const last = newMsgs[newMsgs.length - 1];
                newMsgs[newMsgs.length - 1] = { ...last, showFeedback: true, version };
                return newMsgs;
            });
            eventSource.close();
        });

        console.log(version);
        if(version === null){
            const fetched = await fetchVersion(conversationId);
            setVersion(fetched);
        }

    };

    return (
        <div style={{ display: 'flex', flexDirection: 'column', height: '100%' }}>
            <h3>  Chatbot {version ? `(Version ${version})` : <span style={{ fontStyle: 'italic', color: '#888' }}>Loading version...</span>} </h3>
            <div style={{
                flexGrow: 1,
                overflowY: 'auto',
                border: '1px solid #ccc',
                padding: '10px',
                backgroundColor: '#f9f9f9',
                borderRadius: '8px',
                marginBottom: '10px'
            }}>
                {messages.map((m, i) => (
                    <div key={i}>
                        <MessageBubble message={m.text} sender={m.sender} />
                        {m.sender === 'bot' && m.showFeedback && version && (
                            <FeedbackForm
                                message={m.text}
                                userMessage={messages[i - 1]?.text || ''}
                                conversationId={conversationId!}
                                version={version}
                                clearFeedbackFlags={clearFeedbackFlags}
                                onFeedbackSubmitted={() => setClearFeedbackFlags(false)}
                            />
                        )}
                    </div>
                ))}
            </div>
            <div style={{ display: 'flex', gap: '10px' }}>
                <input
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    onKeyDown={(e) => {
                        if (e.key === 'Enter') handleSend();
                    }}
                    placeholder="Type your message..."
                    style={{
                        flex: 1,
                        padding: '10px',
                        borderRadius: '5px',
                        border: '1px solid #ccc',
                        fontSize: '16px'
                    }}
                />
                <button
                    onClick={handleSend}
                    style={{
                        padding: '10px 15px',
                        fontSize: '16px',
                        borderRadius: '5px',
                        backgroundColor: '#007bff',
                        color: 'white',
                        border: 'none',
                        cursor: 'pointer'
                    }}
                >
                    Send
                </button>
                <button
                    onClick={handleWebSearch}
                    style={{
                        padding: '10px 15px',
                        fontSize: '16px',
                        borderRadius: '5px',
                        backgroundColor: searchWebMode ? '#28a745' : '#007bff',
                        color: 'white',
                        border: 'none',
                        cursor: 'pointer'
                    }}
                >
                    {searchWebMode ? 'Web Search: ON' : 'Search Web'}
                </button>
                <label style={{
                    padding: '10px 15px',
                    fontSize: '16px',
                    borderRadius: '5px',
                    backgroundColor: '#007bff',
                    color: 'white',
                    border: 'none',
                    cursor: 'pointer'
                }}>
                    Upload File
                    <input
                        type="file"
                        style={{ display: 'none' }}
                        onChange={handleFileUpload}
                    />
                </label>
            </div>
        </div>
    );
}
