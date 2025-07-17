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

"""
This test file verifies the behavior of all major data models defined in schemas.py.

We’re testing:
- That each model can be successfully created with valid input.
- That models can be serialized to dict/JSON and then deserialized back (round-trip).
- That invalid or incomplete input raises the correct validation errors.
- That optional fields and nested data behave as expected.

The goal is to make sure the schemas are reliable when used in API requests/responses,
and that they fail gracefully when given bad data.
"""

# Test serialization and deserialization of a valid Transition model.
def test_transition_round_trip():
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


# Test invalid Transition (too short from_state).
def test_transition_invalid_min_length():
    with pytest.raises(ValidationError):
        Transition(
            from_state="x",
            to_state="end",
            essential_for="Admin",
            optional_for="Guest"
        )


# Test RequestSchema with valid data.
def test_request_schema_valid():
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


# Test RequestSchema with empty transitions list (invalid).
def test_request_schema_empty_transitions():
    with pytest.raises(ValidationError):
        RequestSchema(transitions=[], personas=["admin"])


# Test ResponseSchema round-trip and optional fields.
def test_response_schema_with_optional():
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


# Test BaseError and its subclasses.
def test_persona_error_defaults():
    err = PersonaError(message="Persona not recognized", error_type="invalid_persona")
    assert err.status == "error"
    assert err.error_type == "invalid_persona"


# Test TransitionError inherits correctly.
def test_transition_error_defaults():
    err = TransitionError(message="Transition missing required field", error_type="invalid_transition")
    assert err.status == "error"
    assert err.error_type == "invalid_transition"


# Test LLMUnsatisfiedError with suggestions.
def test_llm_unsatisfied_with_suggestions():
    err = LLMUnsatisfiedError(
        message="Unable to generate due to insufficient context",
        suggestions=["Provide more details"]
    )
    assert len(err.suggestions) == 1


# Test UserInputSchema requires non-empty text.
def test_user_input_required():
    with pytest.raises(ValidationError):
        UserInputSchema(text="")


# Test AudioTranscriptionResponse serialization.
def test_audio_transcription_success():
    data = {
        "status": "success",
        "text": "Test message",
        "confidence": 0.98
    }
    obj = AudioTranscriptionResponse(**data)
    assert obj.text == "Test message"
    assert obj.status == "success"


# Test AudioTranscriptionResponse with error message.
def test_audio_transcription_error():
    obj = AudioTranscriptionResponse(status="error", error_message="Audio unclear")
    assert obj.error_message == "Audio unclear"
    assert obj.status == "error"