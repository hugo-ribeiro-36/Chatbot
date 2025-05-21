import React, { useEffect, useState } from 'react';
import axios from 'axios';

type Props = {
    onSelectConversation: (id: string) => void;
    selectedId: string | null;
};

type Conversation = {
    id: string;
};

export default function Sidebar({ onSelectConversation, selectedId }: Props) {
    const [conversations, setConversations] = useState<Conversation[]>([]);

    const fetchConversations = async () => {
        try {
            const res = await axios.get('http://localhost:8000/api/v1/conversations');
            setConversations(res.data);
        } catch (err) {
            console.error('Failed to fetch conversations', err);
        }
    };

    const createNewConversation = async () => {
        try {
            const res = await axios.post('http://localhost:8000/api/v1/conversations');
            const newId = res.data.id;

            // Wait for the user to send a message first before refetching the sidebar list
            onSelectConversation(newId);

        } catch (err) {
            console.error('Failed to create new conversation', err);
        }
    };

    useEffect(() => {
        const fetchConversations = async () => {
            try {
                const res = await axios.get('http://localhost:8000/api/v1/conversations/');
                const allConversations = res.data;

                // For each conversation, fetch its messages and only keep those that have messages
                const filtered: Conversation[] = [];

                for (const convo of allConversations) {
                    const messagesRes = await axios.get(`http://localhost:8000/api/v1/conversations/${convo.id}/messages`);
                    if (messagesRes.data && messagesRes.data.length > 0) {
                        filtered.push(convo);
                    }
                }

                setConversations(filtered);
            } catch (err) {
                console.error('Failed to fetch conversations', err);
            }
        };

        // Initial fetch
        fetchConversations();

        // Event listener for refresh signal
        const handler = () => fetchConversations();
        window.addEventListener("conversationUpdated", handler);

        return () => {
            window.removeEventListener("conversationUpdated", handler);
        };
    }, []);

    return (
        <div style={{ width: '250px', borderRight: '1px solid #ccc', padding: '10px', background: '#f9f9f9' }}>
            <h4 style={{ marginBottom: '10px' }}>Conversations</h4>
            <button
                onClick={createNewConversation}
                style={{
                    background: '#007bff',
                    color: 'white',
                    padding: '6px 10px',
                    border: 'none',
                    borderRadius: '4px',
                    marginBottom: '15px',
                    cursor: 'pointer',
                    width: '100%',
                }}
            >
                + New Chat
            </button>
            <ul style={{ listStyle: 'none', paddingLeft: 0 }}>
                {conversations.map((conversation) => (
                    <li key={conversation.id} style={{ marginBottom: '6px' }}>
                        <button
                            onClick={() => onSelectConversation(conversation.id)}
                            style={{
                                width: '100%',
                                backgroundColor: conversation.id === selectedId ? '#007bff' : '#fff',
                                color: conversation.id === selectedId ? '#fff' : '#333',
                                border: '1px solid #ccc',
                                borderRadius: '4px',
                                padding: '6px',
                                cursor: 'pointer',
                                textAlign: 'left',
                                overflow: 'hidden',
                                textOverflow: 'ellipsis',
                                whiteSpace: 'nowrap',
                            }}
                        >
                            {conversation.id.slice(0, 8)}
                        </button>
                    </li>
                ))}
            </ul>
        </div>
    );
}
