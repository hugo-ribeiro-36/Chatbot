import unittest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

class TestChatbotStream(unittest.TestCase):

    def test_version_endpoint(self):
        # First create a new conversation
        create_resp = client.post("/api/v1/conversations")
        self.assertEqual(create_resp.status_code, 200)
        convo_id = create_resp.json()["id"]

        # Then check that we can fetch its version
        resp = client.get(f"/api/v1/chatbot/version?convo_id={convo_id}")
        self.assertEqual(resp.status_code, 200)
        self.assertIn("version", resp.json())

    def test_chatbot_stream_response(self):
        create_resp = client.post("/api/v1/conversations")
        convo_id = create_resp.json()["id"]
        msg = "Hello"
        with client.stream("GET", f"/api/v1/chatbot/stream?convo_id={convo_id}&message={msg}") as resp:
            self.assertEqual(resp.status_code, 200)

    def test_chatbot_web_response(self):
        create_resp = client.post("/api/v1/conversations")
        convo_id = create_resp.json()["id"]
        msg = "Search something online"
        with client.stream("GET", f"/api/v1/chatbot/web?convo_id={convo_id}&message={msg}") as resp:
            self.assertEqual(resp.status_code, 200)

if __name__ == "__main__":
    unittest.main()