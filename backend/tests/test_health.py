from api_layer.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_root_returns_200():
    response = client.get("/")

    assert response.status_code == 200


def test_root_returns_expected_message():
    response = client.get("/")

    assert response.json() == {
        "message": "Simple AI Chatbot API is running."
    }
