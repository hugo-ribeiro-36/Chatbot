import React, { useEffect, useState } from "react";
import axios from "axios";
import "./Dashboard.css";

const Dashboard = () => {
    const [summary, setSummary] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        axios.get("http://localhost:8000/api/v1/analytics/summary")
            .then(res => {
                setSummary(res.data);
                setLoading(false);
            })
            .catch(err => {
                console.error("Failed to fetch analytics:", err);
                setLoading(false);
            });
    }, []);

    return (
        <div className="dashboard-container">
            <h2>📊 Chatbot Performance Dashboard</h2>
            <button
                onClick={() => {
                    window.open("http://localhost:8000/api/v1/analytics/summary/export", "_blank");
                }}
                style={{ marginBottom: "20px", padding: "10px", cursor: "pointer" }}
            >
                📥 Export Summary as CSV
            </button>
            {loading ? <p>Loading...</p> : (

                <table className="dashboard-table">
                    <thead>
                    <tr>
                        <th>Version</th>
                        <th>Total Feedback</th>
                        <th>Thumbs Up</th>
                        <th>Thumbs Down</th>
                        <th>Average Score</th>
                        <th>Score Ratio</th>
                    </tr>
                    </thead>
                    <tbody>
                    {summary.map((row, idx) => (
                        <tr key={idx}>
                            <td>{row.version}</td>
                            <td>{row.total_feedback}</td>
                            <td>{row.thumbs_up}</td>
                            <td>{row.thumbs_down}</td>
                            <td>{row.average_score}</td>
                            <td>{row.score_ratio}</td>
                        </tr>
                    ))}
                    </tbody>
                </table>
            )}
        </div>
    );
};

export default Dashboard;
