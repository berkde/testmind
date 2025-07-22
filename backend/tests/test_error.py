"""
Unit tests for error.py models (PersonaError, TransitionError).

These tests verify:
- Correct serialization/deserialization.
- Default 'status' field behavior.
- Validation errors for missing required fields.
"""

import pytest
from pydantic import ValidationError
from backend.app.models.error import PersonaError, TransitionError


def test_persona_error_round_trip():
    """Test serialization and deserialization of PersonaError."""
    original = PersonaError(message="Invalid persona ID")
    data = original.model_dump()
    restored = PersonaError.model_validate(data)
    assert restored == original
    assert restored.status == "error"


def test_transition_error_round_trip():
    """Test serialization and deserialization of TransitionError."""
    original = TransitionError(message="Transition format is incorrect")
    data = original.model_dump()
    restored = TransitionError.model_validate(data)
    assert restored == original
    assert restored.status == "error"


def test_persona_error_missing_message():
    """Test validation error when 'message' is missing in PersonaError."""
    with pytest.raises(ValidationError):
        PersonaError.model_validate({})


def test_transition_error_missing_message():
    """Test validation error when 'message' is missing in TransitionError."""
    with pytest.raises(ValidationError):
        TransitionError.model_validate({})
