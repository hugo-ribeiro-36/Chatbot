import unittest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

class TestConversations(unittest.TestCase):

    def test_create_conversation(self):
        response = client.post("/api/v1/conversations")
        self.assertEqual(response.status_code, 200)
        self.assertIn("id", response.json())

    def test_get_all_conversations(self):
        response = client.get("/api/v1/conversations")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)

    def test_get_conversation_messages_empty(self):
        create_res = client.post("/api/v1/conversations")
        convo_id = create_res.json()["id"]
        msg_res = client.get(f"/api/v1/conversations/{convo_id}/messages")
        self.assertEqual(msg_res.status_code, 200)
        self.assertEqual(msg_res.json(), [])

if __name__ == "__main__":
    unittest.main()