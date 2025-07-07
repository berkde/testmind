import sys
import os

# Ensure the Python path includes the root project directory (so we can import 'app')
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from fastapi.testclient import TestClient
from backend.app.api.endpoints import app


# Create a test client to simulate HTTP requests to the API.
client = TestClient(app)


# TEST: Validate request with essential and optional personas.
def test_generate_matrix_success():
    """
    Test that /generate-matrix returns a 200 OK and a successful response
    when given valid input with transitions and personas.
    """
    response = client.post("/generate-matrix", json={
        "transitions": [
            {
                "from": "Drafted",
                "to": "Published",
                "essential_for": "Admin",
                "optional_for": ["Editor"]
            }
        ],
        "personas": ["Admin", "Editor", "Visitor"]
    })

    # Make sure the request was successful.
    assert response.status_code == 200

    # Parse the JSON response and check structure.
    data = response.json()
    assert data["status"] == "success"
    assert "llm_text_response" in data


# TEST: Invalid request (empty transitions and personas).
def test_generate_matrix_invalid_request():
    """
    Test that the API returns a 422 Unprocessable Entity when the
    input is missing required values or improperly structured.
    """
    response = client.post("/generate-matrix", json={
        "transitions": [],
        "personas": []
    })

    # FastAPI should reject this request due to schema validation.
    assert response.status_code == 422
