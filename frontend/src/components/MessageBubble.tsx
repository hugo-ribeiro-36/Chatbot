import React from 'react';

type Props = {
    message: string;
    sender: 'user' | 'bot';
};

const MessageBubble: React.FC<Props> = ({ message, sender }) => {
    const isUser = sender === 'user';

    return (
        <div style={{ display: 'flex', justifyContent: isUser ? 'flex-end' : 'flex-start' }}>
            <div
                style={{
                    backgroundColor: isUser ? '#dcf8c6' : '#fff',
                    color: '#000',
                    padding: '10px',
                    margin: '5px',
                    borderRadius: '10px',
                    maxWidth: '70%',
                    boxShadow: '0 1px 2px rgba(0,0,0,0.1)',
                }}
            >
                {message}
            </div>
        </div>
    );
};

export default MessageBubble;