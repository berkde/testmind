import pytest
from unittest.mock import AsyncMock
# from fastapi.testclient import TestClient
# from backend.app import main

@pytest.fixture(scope="module")
def test_client():
    """
    Provides a TestClient instance to test FastAPI routes.
    Scope is 'module' to reuse it within each test file.

    Note: This is a placeholder. In a real setup, you would import your FastAPI app.
    """
    # Placeholder for when the app is properly set up
    # from app import main
    # client = TestClient(main)
    # yield client

    yield None

@pytest.fixture(autouse=True)
def mock_openai_chat_completions(monkeypatch):
    """
    Automatically mock OpenAI chat completions for all tests to avoid real API calls.
    """
    class DummyAsyncResponse:
        def __aiter__(self):
            # Simulate a streaming response with a single dummy message
            async def gen():
                yield {"choices": [{"message": {"content": "Mocked LLM response"}}]}
            return gen()

    # Patch the async OpenAI chat completion call used by LlamaIndex
    monkeypatch.setattr(
        "openai.resources.chat.completions.Completions.create",
        AsyncMock(return_value=DummyAsyncResponse())
    )