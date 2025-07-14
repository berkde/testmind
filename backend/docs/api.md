# POST /mind Documentation

### Table of Contents

---

1. [/mind](#post-mind)
2. [Expected Behavior](#expected-behavior)
3. [License](#License)
4. [Contact](#Contact)


---

## [POST /mind](#/mind)

## Purpose & Use Case

The /mind endpoint accepts natural language input from the user in the form of project context (e.g., state transitions, personas, test matrix details) and returns a generated test combination matrix and natural language response.

This endpoint provides the frontend UI with an optimized test combinations table, summary, and improvement suggestions for display.

The endpoint acts as the main AI-driven interface, allowing the user to request matrix generation or general conversation-like explanations or suggestions in free-text form.

## Endpoint Implementation

- **Module**: `backend/app/api/endpoints.py`
- **Author**: testMind
- **Copyright**: © 2025 testMind

## POST /mind METHOD

**Endpoint:** `POST /mind`

**Description:**  Accepts natural language input describing project context and returns a generated test combinations matrix (if applicable) or a conversational reply.

**Request:**
- Method: `POST`
- Consumes: JSON
- Produces: JSON
- Body: JSON object of type UserRequestSchema containing a single property: text (string)

**Response:**
- Status Codes:
  - 200 OK: Successful response with one of the following statuses in JSON: "conversation", "success", "unsatisfied", "error"
  - 500 Internal Server Error: Server error with detailed error message and traceback
- Produces: JSON
- Body: JSON object whose structure varies by status field value (see table below)

| Parameter / Request Field | Data Type                      | HTTP Status Code(s)             | Description                                                                                                         |  
|---------------------------|--------------------------------|--------------------------------|---------------------------------------------------------------------------------------------------------------------|  
| `user_input`              | JSON Object with field `text` (string) | 200 OK                         | JSON object with a single field `text` containing string input with project context, personas, and transitions.  |  
 
| Parameter / Response Field | Data Type                      | HTTP Status Code(s) | Description                                                                            |  
|---------------------------|--------------------------------|---------------|----------------------------------------------------------------------------------------|   
| `status`                   | String                        | 200 OK        | Indicates the response status: `"conversation"`, `"success"`, `"unsatisfied"`, `"error"` |  
| `response`                 | String (optional)             | 200 OK        | Present when `status` is `"conversation"`, contains chatbot reply message              |  
| `conversation_context`     | Object (optional)             | 200 OK        | Present when `status` is `"conversation"`, contains context info to maintain session state |  
| `summary`                  | String (optional)             | 200 OK        | Present when `status` is `"success"`, summary of generated matrix              |  
| `recommendations`          | String or null (optional)     | 200 OK        | Present when `status` is `"success"`, suggestions for improving test coverage          |  
| `matrix_data`              | Object (optional)             | 200 OK        | Present when `status` is `"success"`, nested dict with transitions and persona status data |  
| `error_message`            | String (optional)             | 200 OK | Present when `status` is `"error"`, contains error description                         |  
| `traceback`                | String (optional)             | 500 Internal Server Error | Present only in `500 Internal Server Error` responses, contains error stack trace for debugging |

## [Expected Behavior](#Expected_Behavior)

**Example Request:**

{
  "text": "Generate a test matrix for a project management app. Transitions: - from: backlog, to: in-progress, essential_for: developer, optional_for: manager - from: in-progress, to: review, essential_for: developer, optional_for: qa - from: review, to: done, essential_for: qa, optional_for: manager - from: done, to: archived, essential_for: manager, optional_for: admin Personas: - developer - manager - qa - admin"
}

**Example Response:**

{
    "status": "success",
    "summary": "The generated test matrix covers transitions between different stages (backlog, in-progress, review, done, archived) with respective roles (developer, manager, qa, admin) and their statuses.\n\nThe matrix includes 4 test cases, each specifying the status of roles during the transition stages. This aligns with the provided information.\n\nRecommendations to enhance the test results:\n1. **Include Edge Cases**: Incorporate test cases that cover extreme or boundary conditions to ensure the system behaves correctly under all scenarios.\n\n2. **Cross-Role Testing**: Introduce test cases where roles interact or hand over tasks to each other to validate communication and coordination between different roles.\n\n3. **Data Validation Testing**: Verify that the data being transferred between stages is accurate and consistent by including test cases to validate data integrity.\n\n4. **Regression Testing**: Implement regression testing to ensure that changes in one stage do not adversely affect the functionality of previous stages.\n\n5. **Exploratory Testing**: Conduct exploratory testing to discover any unforeseen issues or usability problems during the transitions.\n\nBy incorporating these recommendations, you can further strengthen the testing process and increase the overall quality of the software.",
    "recommendations": "",
    "matrix_data": {
        "backlog→in-progress": {
            "developer": {
                "status": "Green",
                "id": "G1"
            },
            "manager": {
                "status": "Yellow"
            },
            "qa": {
                "status": "Red"
            },
            "admin": {
                "status": "Red"
            }
        },
        "in-progress→review": {
            "developer": {
                "status": "Green",
                "id": "G2"
            },
            "manager": {
                "status": "Red"
            },
            "qa": {
                "status": "Yellow"
            },
            "admin": {
                "status": "Red"
            }
        },
        "review→done": {
            "developer": {
                "status": "Red"
            },
            "manager": {
                "status": "Yellow"
            },
            "qa": {
                "status": "Green",
                "id": "G3"
            },
            "admin": {
                "status": "Red"
            }
        },
        "done→archived": {
            "developer": {
                "status": "Red"
            },
            "manager": {
                "status": "Green",
                "id": "G4"
            },
            "qa": {
                "status": "Red"
            },
            "admin": {
                "status": "Yellow"
            }
        }
    }
}

---

## [License](#License)

This project is licensed under the MIT License - see the [License](../../LICENSE) file for details.

##  [Contact](#Contact)

For questions or feedback, please open an issue or contact the project maintainers.
