import React, { useState } from 'react';
import { sendFeedback } from './api.ts';

type Props = {
    message: string;
    userMessage: string;
    conversationId: string | null;
    version: string;
    onFeedbackSubmitted: () => void;
};

export default function FeedbackForm({ message, userMessage, conversationId, version, onFeedbackSubmitted }: Props) {
    const [rating, setRating] = useState<number | null>(null);
    const [comment, setComment] = useState('');
    const [submitted, setSubmitted] = useState(false);
    const [showForm, setShowForm] = useState(false);

    const handleSubmit = async () => {
        if (conversationId && rating !== null) {

            await sendFeedback({
                conversation_id: conversationId,
                version,
                message,
                user_message: userMessage,
                rating,
                comment,
            });
            setSubmitted(true);
            onFeedbackSubmitted();
        }
    };

    if (submitted) return <p style={{ color: 'green' }}>Thank you for your feedback!</p>;

    return (
        <div style={{ marginTop: '5px' }}>
            {!showForm ? (
                <div>
                    <button onClick={() => { setRating(1); setShowForm(true); }}>👍</button>
                    <button onClick={() => { setRating(0); setShowForm(true); }}>👎</button>
                </div>
            ) : (
                <div>
                    <textarea
                        value={comment}
                        onChange={(e) => setComment(e.target.value)}
                        placeholder="Optional comment"
                        rows={2}
                        style={{ width: '100%', marginBottom: '5px' }}
                        onKeyDown={(e) => {
                            if (e.key === 'Enter' && !e.shiftKey) {
                                e.preventDefault();
                                handleSubmit();
                            }
                        }}
                    />
                    <button onClick={handleSubmit}>Submit Feedback</button>
                </div>
            )}
        </div>
    );
}
