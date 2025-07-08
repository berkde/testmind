# TestMind Backend Tests

This directory contains tests for the TestMind backend system.

## Running Tests

### Option 1: Using pytest (Recommended for IDE)

Run all tests:
```bash
python3 -m pytest tests/ -v
```

Run a specific test:
```bash
python3 -m pytest tests/test_handler.py::test_handler_basic_functionality -v
```

### Option 2: Using the standalone script

Run the standalone test script:
```bash
python3 -m app.test_handler
```

## Test Files

- `test_handler.py` - Pytest tests for the TestMindHandler workflow
  - `test_handler_basic_functionality()` - Tests basic matrix generation
  - `test_handler_error_handling()` - Tests error handling with invalid input
  - `test_handler_complex_input()` - Tests with more complex input scenarios

## Configuration

The `pytest.ini` file in the root directory configures:
- Async test support with `asyncio_mode = auto`
- Test discovery patterns
- Warning filters for deprecation warnings
- Verbose output by default

## Dependencies

Make sure you have the required testing dependencies installed:
```bash
pip install pytest pytest-asyncio pytest-cov
```

## Notes

- The tests use real API calls to OpenAI, so they require valid API credentials
- Tests may take 15-30 seconds to complete due to API latency
- The standalone script (`app/test_handler.py`) is for manual testing and debugging
- The pytest tests (`tests/test_handler.py`) are for automated testing and CI/CD 