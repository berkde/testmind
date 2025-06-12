import pytest

def test_simple():
    """A simple test to verify pytest is working."""
    assert True, "This test should always pass"

if __name__ == "__main__":
    pytest.main(["-v", "test_simple.py"])