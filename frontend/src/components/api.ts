import axios from 'axios';

const api = axios.create({
    baseURL: 'http://localhost:8000/api/v1',
});

export const createConversation = async (): Promise<string> => {
    const res = await axios.post('http://localhost:8000/api/v1/conversations');
    return res.data.id;
};

export const listConversations = async () => {
    const res = await api.get('/conversations');
    return res.data;
};

export const getConversationMessages = async (conversationId: string) => {
    const res = await api.get(`/conversations/${conversationId}/messages`);
    return res.data;
};


export const sendFeedback = async (data: {
    conversation_id: string;
    version: string;
    message: string;
    user_message: string;
    rating: number;
    comment?: string;
}) => {
    await api.post('/feedback', data);
};

export const fetchVersion = async (conversationId: string) => {
    const res = await api.get(`/chatbot/version?convo_id=${conversationId}`);
    return res.data.version;
};