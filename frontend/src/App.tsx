import React, { useEffect, useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import ChatWindow from './components/ChatWindow.tsx';
import Dashboard from './pages/Dashboard.tsx';
import Sidebar from "./components/ConversationList.tsx";
import axios from 'axios';

const headerStyle = {
    backgroundColor: '#f8f8f8',
    padding: '10px 20px',
    borderBottom: '1px solid #ccc',
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
};

const linkStyle = {
    marginRight: '15px',
    textDecoration: 'none',
    color: '#333',
    fontWeight: 'bold',
};

function App() {
    const [conversationId, setConversationId] = React.useState<string | null>(null);

    return (
        <Router>
            <div style={{ height: '100vh', display: 'flex', flexDirection: 'column' }}>
                {/* Top Navigation */}
                <div style={headerStyle}>
                    <h2 style={{ margin: 0 }}>Chatbot</h2>
                    <nav style={{ marginTop: '5px' }}>
                        <Link to="/" style={{ marginRight: '10px' }}>Chat</Link>
                        <Link to="/dashboard">Dashboard</Link>
                    </nav>
                </div>

                {/* Main Content */}
                <div style={{ display: 'flex', height: '100vh' }}>
                    <Sidebar
                        onSelectConversation={setConversationId}
                        selectedId={conversationId}
                    />
                    <div style={{ flex: 1, padding: '20px' }}>
                        <Routes>
                            <Route path="/dashboard" element={<Dashboard />} />
                            <Route path="*" element={<ChatWindow conversationId={conversationId} setConversationId={setConversationId} />} />
                        </Routes>
                    </div>
                </div>
            </div>
        </Router>
    );
}

export default App;
