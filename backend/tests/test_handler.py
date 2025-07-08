#!/usr/bin/env python3
"""
Pytest tests for TestMindHandler
Run these tests to verify the workflow functionality.
"""

import pytest
import logging
from ..app.services.handler import TestMindHandler

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

@pytest.mark.asyncio
async def test_handler_basic_functionality():
    """Test the TestMindHandler with basic input."""

    test_input = """
    Generate a test matrix for the following transitions and personas.

    Transitions:
    - from: login, to: dashboard, essential_for: admin, optional_for: guest
    - from: dashboard, to: logout, essential_for: admin, optional_for: guest

    Personas:
    - admin
    - guest
    """

    handler = TestMindHandler(timeout=300)

    result = await handler.run(test_input)

    assert result is not None
    assert isinstance(result, dict)

    if result.get('matrix_data'):
        assert result.get('matrix_data') is not None
        assert isinstance(result.get('matrix_data'), dict)
        assert len(result.get('matrix_data', {})) > 0

        matrix_data = result.get('matrix_data', {})
        assert 'login→dashboard' in matrix_data
        assert 'dashboard→logout' in matrix_data

        for transition_data in matrix_data.values():
            assert 'admin' in transition_data
            assert 'guest' in transition_data

    assert result.get('summary') is not None
    assert isinstance(result.get('summary'), str)
    assert len(result.get('summary', '')) > 0

@pytest.mark.asyncio
async def test_handler_error_handling():
    """Test the TestMindHandler with invalid input."""

    test_input = "This is not a valid test input"

    handler = TestMindHandler(timeout=300)

    result = await handler.run(test_input)

    assert result is not None
    assert isinstance(result, dict)

    if result.get('status') == 'error':
        assert result.get('message') is not None
        assert isinstance(result.get('message'), str)
    else:
        assert not result.get('matrix_data')

@pytest.mark.asyncio
async def test_handler_complex_input():
    """Test the TestMindHandler with more complex input."""

    test_input = """
    Generate a test matrix for the following transitions and personas.

    Transitions:
    - from: login, to: dashboard, essential_for: admin, optional_for: guest
    - from: dashboard, to: settings, essential_for: admin, optional_for: user
    - from: settings, to: logout, essential_for: admin, optional_for: user

    Personas:
    - admin
    - guest
    - user
    """

    handler = TestMindHandler(timeout=300)

    result = await handler.run(test_input)

    assert result is not None
    assert isinstance(result, dict)

    if result.get('matrix_data'):
        assert result.get('matrix_data') is not None
        assert isinstance(result.get('matrix_data'), dict)
        assert len(result.get('matrix_data', {})) > 0

        matrix_data = result.get('matrix_data', {})
        assert 'login→dashboard' in matrix_data
        assert 'dashboard→settings' in matrix_data
        assert 'settings→logout' in matrix_data

        for transition_data in matrix_data.values():
            assert 'admin' in transition_data
            assert 'guest' in transition_data or 'user' in transition_data 