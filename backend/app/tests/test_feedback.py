import unittest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

class FeedbackTests(unittest.TestCase):
    def test_submit_feedback(self):
        payload = {
            "conversation_id": "test-id",
            "version": "A",
            "message": "This is a test response.",
            "user_message": "Test input",
            "rating": 1,
            "comment": "Good job"
        }
        response = client.post("/api/v1/feedback", json=payload)
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()