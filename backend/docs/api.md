# TestMind API Endpoints - Documentation

### Table of Contents

---

1. [/mind](#post-mind)
2. [/transcribe-audio](#post-transcribe-audio)
3. [/health](#get-health)
4. [License](#License)
5. [Contact](#Contact)

---

## [POST /mind](#/mind)

## Purpose & Use Case

The /mind endpoint is the central AI-driven interface for all TestMind interactions. It accepts natural language input describing project context (e.g., state transitions, personas, test matrix details) and processes it to either continue a conversation or generate a structured test combinations matrix.

The endpoint returns contextual conversational responses, summaries, optimized test matrices, and improvement recommendations—providing the frontend UI with data and explanations to display to the user.

## Endpoint Implementation

- **Module**: `backend/app/api/endpoints.py`
- **Author**: testMind
- **Copyright**: © 2025 testMind

## POST /mind METHOD

**Endpoint:** `POST /mind`

**Description:** POST /mind accepts user input text and returns a JSON response that either continues the conversation, provides a summary with recommendations and matrix data, or reports errors.

**Request:**
- Method: `POST`
- Consumes: application/json 
- Produces: application/json 
- Body: JSON object of type UserRequestSchema containing:
  - text (string): The user's input text

| **Parameter/Request Field** | **Data Type** | **Required** | **Description**                    |
|-----------------------------|---------------|--------------|------------------------------------|
| `text`                      | string        | Yes          | User input text (minimum length 1) |

**Response:**
- Status Codes:
  - 200 OK: Successful response with one of the following statuses in JSON: "conversation", "success", "error"
  - 500 Internal Server Error: Server error with a generic error message 
- Produces: application/json 
- Body: JSON object whose structure varies depending on the value of the status field (see table below)

| **Response Field** | **Data Type** | **HTTP Status** | **Description**                                                                          |
|-----------------------------|---------------|-----------------|------------------------------------------------------------------------------------------|
| `status`                    | string        | 200 OK          | Indicates the type of response: `"conversation"`, `"success"`, `"unknown"`, or `"error"` |
| `response`                  | string        | 200 OK          | Present when `status` is `"conversation"`; a natural language reply from the agent.      |
| `conversation_context`      | object (JSON) | 200 OK          | Present when `status` is `"conversation"`; context for follow-up interactions.           |
| `summary`                   | string        | 200 OK          | Present when `status` is `"success"`; natural language summary of matrix.                |
| `recommendations`           | array or null | 200 OK          | Present when `status` is `"success"`; suggestions for test strategy improvement.         |
| `matrix_data`               | object (JSON) | 200 OK          | Present when `status` is `"success"`; generated test matrix content.                     |
| `matrix_statistics`         | object (JSON) | 200 OK          | Present when `status` is `"success"`; numeric stats about the generated matrix.          |
| `error_message`             | string        | 200 OK / 500    | Present when `status` is `"error"` or `"unknown"`; describes the issue encountered.      |


## POST /mind Expected Behavior

**Example Request:**

{
  "text": "please generate me a test case combinations matrix for a posting app. the personas are visitor, registered user, and website admin. the transition states are from nothing to read post (essential for visitor), another transition is from post drafted to post published (essential for registered user, optional for admin), and a third transition is from post published to post pinned (essential for registered user, optional for admin)"
}

**Example Response:**

{"status":"success","summary":"\n        # Summary\n        The generated test case combinations matrix is tailored for a posting app with three personas: visitor, registered user, and website admin. The matrix includes transitions from \"nothing\" to \"read post\" (essential for visitor), from \"post drafted\" to \"post published\" (essential for registered user, optional for admin), and from \"post published\" to \"post pinned\" (essential for registered user, optional for admin). The matrix consists of 3 essential test cases covering the required transitions for the personas.\n\n        # Matrix Statistics\n        - Total combinations: 9 (3 transitions × 3 personas)\n        - Essential combinations (Green): 3 - Selected for execution with test IDs G1, G2, G3\n        - Redundant combinations (Yellow): 0 - No optional combinations provided\n        - Prohibited combinations (Red): 6 - Combinations where transitions are prohibited for specific personas\n\n        # Explanation\n        The matrix covers all specified transitions for the personas as follows:\n        1. From \"nothing\" to \"read post\": Essential for the visitor (G1), prohibited for registered user and website admin.\n        2. From \"post drafted\" to \"post published\": Essential for the registered user (G2), prohibited for visitor and website admin.\n        3. From \"post published\" to \"post pinned\": Essential for the registered user (G3), prohibited for visitor and website admin.\n        \n        The matrix ensures that each persona can only perform the transitions relevant to their role. Prohibited combinations prevent unauthorized actions, maintaining the integrity of the workflow.\n\n        # Recommendations\n        - Test Scenario 1 (G1): Verify that a visitor can successfully transition from \"nothing\" to \"read post\".\n        - Test Scenario 2 (G2): Validate that a registered user can move a post from \"post drafted\" to \"post published\".\n        - Test Scenario 3 (G3): Ensure that a registered user can pin a post after it has been published.\n        \n        # Quality Check\n        - All specified transitions are covered in the matrix.\n        - Essential and prohibited relationships are correctly mapped.\n        - No optional combinations were provided, ensuring focus on essential test cases.\n        - The test cases are actionable and aligned with the user's requirements.","recommendations":"","matrix_data":{"nothing→read post":{"visitor":{"status":"Essential","id":"G1"},"registered user":{"status":"Prohibited"},"website admin":{"status":"Prohibited"}},"post drafted→post published":{"visitor":{"status":"Prohibited"},"registered user":{"status":"Essential","id":"G2"},"website admin":{"status":"Prohibited"}},"post published→post pinned":{"visitor":{"status":"Prohibited"},"registered user":{"status":"Essential","id":"G3"},"website admin":{"status":"Prohibited"}}},"matrix_statistics":{"total_combinations":9,"essential_combinations":3,"optional_combinations":0,"prohibited_combinations":6,"total_transitions":3,"total_personas":3}}

---

## [POST /transcribe-audio](#transcribe-audio)

## Purpose & Use Case

The /transcribe-audio endpoint accepts an audio file upload in various supported formats (WAV, MP3, M4A, etc.) and transcribes the speech within the file to text using speech recognition. 
In the testMind chatbot interface, the client records audio locally (e.g., via microphone input) which is saved as an audio file and then uploaded to this endpoint for transcription. 
The backend processes the uploaded audio file and returns the transcribed text.

## Endpoint Implementation

- **Module**: `backend/app/api/endpoints.py`
- **Author**: testMind
- **Copyright**: © 2025 testMind

## POST /transcribe-audio METHOD

**Endpoint:** `POST /transcribe-audio`

**Description:** 
Uploads an audio file and returns the transcribed text extracted from the speech within the file. Supports multiple common audio formats.

**Request:**
- Method: `POST`
- Consumes: multipart/form-data
- Produces: application/json 
- Body: A single file parameter (audio_file) containing the audio file to transcribe. Supported formats: .wav, .mp3, .m4a, .flac, .ogg, .webm.

| **Parameter/Request Field** | **Data Type** | **Required** | **Description**                                 |
|-----------------------------|---------------|--------------|-------------------------------------------------|
| `audio_file`                | File          | Yes          | The audio file to transcribe. Supported formats: `.wav`, `.mp3`, `.m4a`, `.flac`, `.ogg`, `.webm`. |

**Response:**
- Status Codes:
  - 200 OK: Transcription succeeded or failed with a handled error message
  - 400 Bad Request: File format not supported
- Produces: application/json 
- Body: JSON object with fields that vary depending on whether the transcription was successful or an error occurred (see table below)

| **Response Fields**  | **Data Type** | **HTTP Status**      | **Description**                                                              |
|-------------------------------|---------------|----------------------|------------------------------------------------------------------------------|
| `status`, `text`, `confidence` | JSON Object   | `200 OK`             | **success**: Returns the transcribed text and a confidence score.            |
| `status`, `error_message`     | JSON Object   | `200 OK`             | **error**: Could not understand the audio (e.g., unclear speech).            |
| `status`, `error_message`     | JSON Object   | `200 OK`             | **error**: Speech recognition service error (e.g., API/network failure).     |
| `status`, `error_message`     | JSON Object   | `200 OK`             | **error**: General error during processing (e.g., file read/write failure).  |
| `detail`                      | JSON Object   | `400 Bad Request`     | **error**: File format is not supported. Raised before transcription starts. |

## POST /transcribe-audio Expected Behavior

**Example Request**:

POST /transcribe-audio
Content-Type: multipart/form-data
Body: audio_file = sample.wav

**Example Response**:
{
  "status": "success",
  "text": "Generate the matrix",
  "confidence": 0.8
}
---
## [GET /health](#/health)

## Purpose & Use Case

The purpose of the health check endpoint is to confirm that the testMind backend server is running and able to respond to HTTP requests. 
It is typically used for monitoring, deployment checks, and basic availability testing.

## Endpoint Implementation

- **Module**: `backend/app/api/endpoints.py`
- **Author**: testMind
- **Copyright**: © 2025 testMind

## GET /health METHOD

**Endpoint:** `GET /health`

**Description:** Returns a simple JSON response confirming that the TestMind backend is running and capable of receiving and responding to HTTP requests. Commonly used for monitoring, deployment validation, and basic availability checks. 

**Request:**
- Method: `GET`
- Consumes: none
- Produces: application/json 
- Body: none

| **Parameter/Request Field** | **Data Type** | **Required** | **Description**            |
|-----------------------------|---------------|--------------|----------------------------|
| _None_                      | —             | —            | This endpoint does not require a request body or parameters. |

**Response:**
- Status Codes:
  - 200 OK: Backend is healthy and responsive
  - 500 Internal Server Error: The server failed to respond properly (e.g., application crash or misconfiguration)
- Produces: application/json 
- Body (200 OK): JSON object (see table below)

| **Parametesr/Resposne Field(s)**            | **Response Type** | **HTTP Status**        | **Description**                                                                |
|---------------------------------------------|-------------------|------------------------|--------------------------------------------------------------------------------|
| `status`, `message`, `version`              | JSON Object       | `200 OK`               | **success** – Backend is running and responsive. Includes version info.        |
| Varies (may be plain text or JSON `detail`) | JSON Object or text | `500 Internal Server Error` | **error** – Server failed to respond properly (e.g., crash, misconfiguration). |

## GET /health Expected Behavior

**Example Request**:

GET /health HTTP/1.1
Host: testmind-u11n.onrender.com

**Example Response**:
{
  "status": "healthy",
  "message": "TestMind backend is running",
  "version": "1.0.0"
}
___

## [License](#License)

This project is licensed under the MIT License - see the [License](../../LICENSE) file for details.

##  [Contact](#Contact)

For questions or feedback, please open an issue or contact the project maintainers.
