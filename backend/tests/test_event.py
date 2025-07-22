"""
Unit tests for event.py event models.

Covers:
- Validation of required and optional fields.
- Serialization and deserialization (round-trip).
- Event-specific model logic and schema compliance.
"""

import pytest
from pydantic import ValidationError
from backend.app.models.event import (
    ConversationEvent,
    ConversationResponseEvent,
    GenerateEvent,
    MatrixEvent,
    MatrixAnswerEvent,
    ProgressEvent,
    ErrorEvent
)
from backend.app.models.schemas import RequestSchema, Transition


def test_conversation_event_round_trip():
    """Test creation and round-trip validation of ConversationEvent."""
    data = {"input": "What are the valid states?"}
    obj = ConversationEvent(**data)
    assert obj.model_dump() == data
    assert ConversationEvent.model_validate(data) == obj


def test_conversation_response_event_complete():
    """Test ConversationResponseEvent with all fields populated."""
    data = {
        "response": "Yes, generating matrix.",
        "should_generate_matrix": True,
        "matrix_input": "Generate login matrix",
        "conversation_context": {"step": 2}
    }
    obj = ConversationResponseEvent(**data)
    assert obj.should_generate_matrix is True
    assert obj.matrix_input == "Generate login matrix"


def test_conversation_response_event_missing_required():
    """Test ConversationResponseEvent fails with missing required fields."""
    with pytest.raises(ValidationError):
        ConversationResponseEvent(response="Hi")


def test_generate_event_requires_input():
    """Test GenerateEvent validation for missing required input."""
    with pytest.raises(ValidationError):
        GenerateEvent()


def test_matrix_event_with_valid_request():
    """Test MatrixEvent creation with nested valid RequestSchema."""
    req = RequestSchema(
        transitions=[
            Transition(from_state="Login", to_state="Dashboard", essential_for="admin", optional_for="guest")
        ],
        personas=["admin", "guest"]
    )
    obj = MatrixEvent(request_input=req)
    assert obj.request_input.personas == ["admin", "guest"]


def test_matrix_answer_event_serialization():
    """Test MatrixAnswerEvent serialization and deserialization."""
    data = {
        "matrix_data": {"A->B": {"admin": {"status": "Essential", "id": "T1"}}},
        "explanation": "Generated coverage for admin login"
    }
    obj = MatrixAnswerEvent(**data)
    assert MatrixAnswerEvent.model_validate(obj.model_dump()) == obj


def test_progress_event_message():
    """Test ProgressEvent with message field."""
    obj = ProgressEvent(msg="Now processing transitions...")
    assert obj.msg.startswith("Now processing")


def test_error_event_requires_message():
    """Test ErrorEvent requires 'message' field to be valid."""
    with pytest.raises(ValidationError):
        ErrorEvent()


def test_error_event_round_trip():
    """Test ErrorEvent round-trip serialization and validation."""
    data = {"message": "Something went wrong."}
    obj = ErrorEvent(**data)
    assert obj.model_dump()["message"] == "Something went wrong."
    assert ErrorEvent.model_validate(data) == obj
