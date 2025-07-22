"""
Unit tests for config.py (Settings and AgentModelConfig).

Covers:
- Default settings loading.
- Field validation in AgentModelConfig.
- Singleton access to settings.
- Environment variable override (mocked).
"""

import os
from unittest.mock import patch
import pytest
from pydantic import ValidationError

from backend.app.core.config import (
    AgentModelConfig,
    Settings,
    get_settings,
    get_api_key
)


def test_agent_model_config_valid():
    """Test valid initialization of AgentModelConfig."""
    config = AgentModelConfig(model="gpt-4", temperature=0.7, max_tokens=1000)
    assert config.model == "gpt-4"
    assert config.temperature == 0.7
    assert config.max_tokens == 1000


def test_agent_model_config_invalid_temperature():
    """Test that invalid temperature raises validation error."""
    with pytest.raises(ValidationError):
        AgentModelConfig(model="gpt-4", temperature=1.5, max_tokens=1000)


def test_agent_model_config_invalid_model():
    """Test that invalid model string raises validation error."""
    with pytest.raises(ValidationError):
        AgentModelConfig(model="gpt-2", temperature=0.5, max_tokens=500)


def test_settings_default_agents():
    """Test default Settings instance and agent configs."""
    settings = Settings()
    assert settings.conversation_agent.model == "gpt-4"
    assert settings.answer_agent.max_tokens == 2000


def test_get_settings_returns_singleton():
    """Test that get_settings returns a consistent singleton."""
    s1 = get_settings()
    s2 = get_settings()
    assert s1 is s2


def test_get_api_key_env_var(monkeypatch):
    """Test retrieval of OPENAI_API_KEY from environment."""
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test-key")
    get_api_key.cache_clear()
    assert get_api_key() == "sk-test-key"


def test_get_api_key_returns_none(monkeypatch):
    """Test that get_api_key returns None when env var is missing."""
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    get_api_key.cache_clear()
    assert get_api_key() is None