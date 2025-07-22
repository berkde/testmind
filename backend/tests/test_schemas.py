"""
Unit tests for schemas.py data models.

Covers:
- Serialization and deserialization of core schemas
- Validation errors for bad input
- Default field behavior for optional and inherited types
"""

import pytest
from pydantic import ValidationError
from backend.app.models.schemas import (
    Transition,
    RequestSchema,
    ResponseSchema,
    PersonaError,
    TransitionError,
    LLMUnsatisfiedError,
    UserInputSchema,
    AudioTranscriptionResponse
)


def test_transition_round_trip():
    """Test valid creation and round-trip serialization of Transition model."""
    data = {
        "from_state": "start",
        "to_state": "end",
        "essential_for": "Admin",
        "optional_for": "Guest"
    }
    obj = Transition(**data)
    assert obj.model_dump() == data
    loaded = Transition.model_validate(obj.model_dump())
    assert loaded == obj


def test_transition_invalid_min_length():
    """Test Transition validation failure on short from_state."""
    with pytest.raises(ValidationError):
        Transition(
            from_state="x",
            to_state="end",
            essential_for="Admin",
            optional_for="Guest"
        )


def test_request_schema_valid():
    """Test creation of RequestSchema with valid nested transitions."""
    data = {
        "transitions": [
            {
                "from_state": "login",
                "to_state": "dashboard",
                "essential_for": "admin",
                "optional_for": "guest"
            }
        ],
        "personas": ["admin", "guest"]
    }
    obj = RequestSchema(**data)
    assert len(obj.transitions) == 1
    assert "admin" in obj.personas


def test_request_schema_empty_transitions():
    """Test validation failure when transitions list is empty."""
    with pytest.raises(ValidationError):
        RequestSchema(transitions=[], personas=["admin"])


def test_response_schema_with_optional():
    """Test optional fields and nested tuple structure in ResponseSchema."""
    data = {
        "status": "success",
        "llm_text_response": "Generated matrix successfully",
        "generated_matrix": (
            {"login->dashboard": {"admin": {"status": "Essential", "id": "T1"}}},
            [{"id": "T1", "transition": "login->dashboard", "by": "admin"}]
        ),
        "suggestions": ["Try adjusting your transitions"]
    }
    obj = ResponseSchema(**data)
    serialized = obj.model_dump()
    assert serialized["status"] == "success"
    deserialized = ResponseSchema.model_validate(serialized)
    assert deserialized == obj


def test_persona_error_defaults():
    """Test PersonaError defaults and additional field assignment."""
    err = PersonaError(message="Persona not recognized", error_type="invalid_persona")
    assert err.status == "error"
    assert err.error_type == "invalid_persona"


def test_transition_error_defaults():
    """Test TransitionError inherits BaseError and applies correct fields."""
    err = TransitionError(message="Transition missing required field", error_type="invalid_transition")
    assert err.status == "error"
    assert err.error_type == "invalid_transition"


def test_llm_unsatisfied_with_suggestions():
    """Test LLMUnsatisfiedError model with suggestion list."""
    err = LLMUnsatisfiedError(
        message="Unable to generate due to insufficient context",
        suggestions=["Provide more details"]
    )
    assert len(err.suggestions) == 1


def test_user_input_required():
    """Test validation error when UserInputSchema is given empty string."""
    with pytest.raises(ValidationError):
        UserInputSchema(text="")


def test_audio_transcription_success():
    """Test AudioTranscriptionResponse model with successful status."""
    data = {
        "status": "success",
        "text": "Test message",
        "confidence": 0.98
    }
    obj = AudioTranscriptionResponse(**data)
    assert obj.text == "Test message"
    assert obj.status == "success"


def test_audio_transcription_error():
    """Test AudioTranscriptionResponse model with error message."""
    obj = AudioTranscriptionResponse(status="error", error_message="Audio unclear")
    assert obj.error_message == "Audio unclear"
    assert obj.status == "error"
