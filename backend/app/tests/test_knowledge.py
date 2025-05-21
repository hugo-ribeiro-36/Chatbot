import unittest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

class KnowledgeTests(unittest.TestCase):
    def test_upload_knowledge(self):
        payload = {
            "text": "Test knowledge base content."
        }
        response = client.post("/api/v1/knowledge", json=payload)
        self.assertEqual(response.status_code, 200)

    def test_list_knowledge(self):
        response = client.get("/api/v1/knowledge")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)

if __name__ == '__main__':
    unittest.main()