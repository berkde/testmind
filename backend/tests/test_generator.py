import unittest


class TestGeneratorTest(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()

def test_generate_matrix_endpoint(test_client):
    payload = {
        "transitions": [
            {
                "from_state": "Post Drafted",
                "to_state": "Post Published",
                "essential_for": "RegisteredUser",
                "optional_for": "Admin"
            }
        ],
        "personas": ["RegisteredUser", "Visitor", "Admin"]
    }

    response = test_client.post("/generate-matrix", json=payload)
    assert response.status_code == 200

    data = response.json()
    assert data["status"] == "success"
    assert "generated_matrix" in data
    assert "Mock matrix generated successfully" in data["llm_text_response"]