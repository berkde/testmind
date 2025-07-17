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

"""
This test file covers all Event subclasses defined in event.py.

Each test checks that:
- Models can be created with valid input
- Required fields are enforced
- Serialization/deserialization works correctly
- Optional fields default properly or validate when omitted
"""


# Test basic creation and round-trip of ConversationEvent.
def test_conversation_event_round_trip():
    data = {"input": "What are the valid states?"}
    obj = ConversationEvent(**data)
    assert obj.model_dump() == data
    assert ConversationEvent.model_validate(data) == obj


# Test ConversationResponseEvent with all fields.
def test_conversation_response_event_complete():
    data = {
        "response": "Yes, generating matrix.",
        "should_generate_matrix": True,
        "matrix_input": "Generate login matrix",
        "conversation_context": {"step": 2}
    }
    obj = ConversationResponseEvent(**data)
    assert obj.should_generate_matrix is True
    assert obj.matrix_input == "Generate login matrix"


# Test ConversationResponseEvent with missing required fields.
def test_conversation_response_event_missing_required():
    with pytest.raises(ValidationError):
        ConversationResponseEvent(response="Hi")


# Test GenerateEvent requires input.
def test_generate_event_requires_input():
    with pytest.raises(ValidationError):
        GenerateEvent()


# Test MatrixEvent with valid nested RequestSchema.
def test_matrix_event_with_valid_request():
    req = RequestSchema(
        transitions=[
            Transition(from_state="Login", to_state="Dashboard", essential_for="admin", optional_for="guest")
        ],
        personas=["admin", "guest"]
    )
    obj = MatrixEvent(request_input=req)
    assert obj.request_input.personas == ["admin", "guest"]


# Test MatrixAnswerEvent round-trip.
def test_matrix_answer_event_serialization():
    data = {
        "matrix_data": {"A->B": {"admin": {"status": "Essential", "id": "T1"}}},
        "explanation": "Generated coverage for admin login"
    }
    obj = MatrixAnswerEvent(**data)
    assert MatrixAnswerEvent.model_validate(obj.model_dump()) == obj


# Test ProgressEvent message field.
def test_progress_event_message():
    obj = ProgressEvent(msg="Now processing transitions...")
    assert obj.msg.startswith("Now processing")


# Test ErrorEvent requires message.
def test_error_event_requires_message():
    with pytest.raises(ValidationError):
        ErrorEvent()


# Test ErrorEvent round-trip.
def test_error_event_round_trip():
    data = {"message": "Something went wrong."}
    obj = ErrorEvent(**data)
    assert obj.model_dump()["message"] == "Something went wrong."
    assert ErrorEvent.model_validate(data) == obj