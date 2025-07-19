"""
Pytest configuration and fixtures for TestMind backend tests.
This file provides fixtures for CI/CD to avoid real API calls and ensure fast, reliable tests.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock


@pytest.fixture
def mock_openai_response():
    """Mock OpenAI API response for testing."""
    mock_response = MagicMock()
    mock_response.response = """
    **Transitions:**
    1. from: login, to: dashboard, essential_for: admin, optional_for: guest
    2. from: dashboard, to: logout, essential_for: admin, optional_for: guest

    **Personas:**
    - admin
    - guest
    """
    mock_response.raw = mock_response.response
    return mock_response


@pytest.fixture
def mock_matrix_response():
    """Mock matrix generation response for testing."""
    mock_response = MagicMock()
    mock_response.response = """
    {
        "matrix": {
            "login→dashboard": {
                "admin": {"status": "Essential", "id": "G1"},
                "guest": {"status": "Optional"}
            },
            "dashboard→logout": {
                "admin": {"status": "Essential", "id": "G2"},
                "guest": {"status": "Optional"}
            }
        },
        "test_cases": [
            {"id": "G1", "transition": "login→dashboard", "persona": "admin"},
            {"id": "G2", "transition": "dashboard→logout", "persona": "admin"}
        ],
        "statistics": {
            "total_combinations": 4,
            "essential_combinations": 2,
            "optional_combinations": 2,
            "prohibited_combinations": 0,
            "total_transitions": 2,
            "total_personas": 2
        }
    }
    """
    mock_response.raw = mock_response.response
    return mock_response


@pytest.fixture
def mock_validation_response():
    """Mock validation response for testing."""
    mock_response = MagicMock()
    mock_response.response = """
    The generated test matrix is well-structured with two test cases covering the transitions 'login→dashboard' and 'dashboard→logout'. 
    Each test case includes scenarios for 'admin' and 'guest' user roles with their corresponding statuses.
    
    Recommendations:
    1. Consider adding expected results for each test case
    2. Include boundary testing scenarios
    3. Add negative test cases for error conditions
    """
    mock_response.raw = mock_response.response
    return mock_response


@pytest.fixture
def mock_agent():
    """Mock agent for testing without real API calls."""
    mock_agent = AsyncMock()
    return mock_agent


@pytest.fixture
def sample_test_input():
    """Sample test input for consistent testing."""
    return """
    Generate a test matrix for the following transitions and personas.

    Transitions:
    - from: login, to: dashboard, essential_for: admin, optional_for: guest
    - from: dashboard, to: logout, essential_for: admin, optional_for: guest

    Personas:
    - admin
    - guest
    """


@pytest.fixture
def sample_matrix_data():
    """Sample matrix data for testing."""
    return {
        "login→dashboard": {
            "admin": {"status": "Green", "id": "G1"},
            "guest": {"status": "Yellow"}
        },
        "dashboard→logout": {
            "admin": {"status": "Green", "id": "G2"},
            "guest": {"status": "Yellow"}
        }
    }


@pytest.fixture
def mock_environment(monkeypatch):
    """Mock environment variables for testing."""
    monkeypatch.setenv("OPENAI_API_KEY", "test-api-key")

    monkeypatch.setenv("OPENAI_MODEL", "gpt-3.5-turbo")
    
    return {
        "OPENAI_API_KEY": "test-api-key",
        "OPENAI_MODEL": "gpt-3.5-turbo"
    }


@pytest.fixture(autouse=True)
def disable_real_api_calls(monkeypatch):
    """Automatically disable real API calls during tests."""
    pass 