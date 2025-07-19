# TestMIND 

<div align="center">
  <img src="banners/banner.png" alt="TestMIND Logo" width="200"/>

  [![Backend CI](https://github.com/berkde/testmind/actions/workflows/backend.yml/badge.svg)](https://github.com/berkde/testmind/actions/workflows/backend.yml)
  [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
  [![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
  [![FastAPI](https://img.shields.io/badge/FastAPI-0.68.0+-green.svg)](https://fastapi.tiangolo.com/)
  [![React](https://img.shields.io/badge/React-17.0.2+-blue.svg)](https://reactjs.org/)
  ![OpenAI](https://img.shields.io/badge/-OpenAI-412991?logo=OpenAI&logoColor=white&style=flat-square)
  ![LLaMA](https://img.shields.io/badge/-LLaMA-FF6F00?logo=Meta&logoColor=white)
  ![Render](https://img.shields.io/badge/-Render-46E3B7?logo=Render&logoColor=white)


</div>

## Project Description

**TestMIND** (Test Management, Integration, and Natural Development) is an AI-assisted tool designed to generate structured software test cases from natural language feature descriptions. It bridges the gap between human requirements and automated testing by combining Natural Language Processing (NLP) and rule-based logic.

Our mission is to streamline the software testing process by automatically generating comprehensive test suites from plain English requirements, saving development teams valuable time and ensuring thorough test coverage.

### Why TestMIND?

- **Reduce Manual Test Writing**: Automatically generate test cases from requirements
- **Improve Test Coverage**: Ensure all edge cases and scenarios are considered
- **Standardize Testing Approach**: Create consistent test cases across projects
- **Accelerate Development**: Integrate seamlessly with CI/CD pipelines

---

##  Features

- Generate positive, negative & edge test cases from natural language descriptions
- Support for AllPairs test reduction to optimize test suite size
- Interactive UI to edit, save, and export test suites in various formats
- Visual test coverage feedback and reporting
- Integration with popular testing frameworks and CI/CD pipelines
- Speech-to-Text Support: Voice input and audio file transcription for hands-free interaction

---

##  Tech Stack

| Layer       | Tech                               |
|------------|------------------------------------|
| Backend    | Python, FastAPI, OpenAI            |
| Frontend   | React, JavaScript                  |
| API Access | OpenAI GPT API                     |
| Speech Recognition | Google Web Speech API        |
| Testing    | Pytest, React Testing Library      |
| CI/CD      | GitHub Actions                     |
| Security/Analysis | CodeQL                             |

---

##  Architecture

<details>
<summary>Click to expand</summary>

<pre>
graph TD
A[User (Text/Voice)] --> F[React Frontend (UI)]
F -->|API Request| --> B[FastAPI Backend]
B -->|Prompt| --> C[OpenAI GPT API]
C -->|LLM Output| --> D[Test Case Generator]
D -->|Test Matrix| --> F
F --> A
</pre> </details>

## System Connectivity Diagram

<details>
<summary>Click to expand</summary>

This diagram illustrates how user input flows through the TestMIND system, now deployed on Render. Both the React frontend and FastAPI backend are hosted as separate services on Render, communicating over HTTPS. The backend may call external APIs (OpenAI, HuggingFace) as before.

```mermaid
graph TD
    subgraph User
        A["Web Browser"]
    end
    subgraph Render Frontend
        B["React App (Vite, Static Site)"]
    end
    subgraph Render Backend
        C["FastAPI API Server"]
        D["Pydantic Schemas (Validation)"]
        E["Service Layer (Test Generator, NLP, AllPairs)"]
        F["External APIs (OpenAI, HuggingFace)"]
    end

    A -->|"HTTPS"| B
    B -->|"API Request (HTTPS)"| C
    C --> D
    D --> E
    E --> F
    F --> E
    E -->|"Response (test cases, feedback)"| C
    C -->|"API Response (HTTPS)"| B
    B -->|"Display results"| A

    %% Hosting context
    B -.->|"Hosted on Render (Static Site)"| B
    C -.->|"Hosted on Render (Web Service)"| C
```

*Solid arrows* show the main data flow. *Dashed arrows* indicate hosting context on Render for both frontend and backend services.
</details>

## Repository Structure

<details>
<summary>Click to expand</summary>

<pre>
testmind/
├── backend/
│   ├── __init__.py
│   ├── app/
│   │   ├── __init__.py
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   └── endpoints.py
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   ├── agent.py
│   │   │   ├── config.py
│   │   │   ├── testcase_generator.py
│   │   │   └── workflow.py
│   │   ├── main.py
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── error.py
│   │   │   ├── event.py
│   │   │   └── schemas.py
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   └── handler.py
│   │   ├── utils/
│   │   │   ├── __init__.py
│   │   │   └── all_pairs.py
│   ├── README.md
│   ├── requirements.txt
│   └── tests/
│       ├── __init__.py
│       ├── conftest.py
│       ├── demo_complex_matrix.py
│       ├── demo_matrix.py
│       ├── pytest.ini
│       ├── README.md
│       ├── test_generator.py
│       ├── test_handler.py
│       └── test_simple.py
├── banners/
│   ├── adam.png
│   ├── banner.png
│   ├── berk.png
│   ├── jiawei.png
│   └── lori.png
├── frontend/
│   ├── eslint.config.js
│   ├── index.html
│   ├── package.json
│   ├── public/
│   │   └── banner.png
│   ├── README.md
│   ├── src/
│   │   ├── App.css
│   │   ├── App.jsx
│   │   ├── assets/
│   │   │   ├── adam.png
│   │   │   ├── berk.png
│   │   │   ├── jiawei.png
│   │   │   └── lori.png
│   │   ├── components/
│   │   │   ├── Card.css
│   │   │   ├── Card.jsx
│   │   │   ├── Header.css
│   │   │   └── Header.jsx
│   │   ├── index.css
│   │   ├── main.jsx
│   │   └── pages/
│   │       ├── Contact.css
│   │       ├── Contact.jsx
│   │       ├── Home.css
│   │       └── Home.jsx
│   ├── vite.config.js
├── LICENSE
├── README.md

</pre>
</details>

## TestMIND Interface in Action

<div align="center">
  <img src="banners/1.png" alt="TestMind Interface Screenshot 1" width="1100" style="max-width: 100%; height: auto; border-radius: 0.5rem; margin: auto;"/>
  <br/><br/>
  <img src="banners/2.png" alt="TestMind Interface Screenshot 2" width="1100" style="max-width: 100%; height: auto;border-radius: 0.5rem; margin: auto;"/>
</div>

## Getting Started

### Prerequisites

- Python 3.11
- Node.js 14.x or higher
- OpenAI API key

### Quick Start

1. Clone the repository:
   ```bash
   git clone https://github.com/berkde/testmind.git
   cd testmind
   ```

2. Set up the backend:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Set up the frontend:
   ```bash
   cd ../frontend
   npm install
   ```

4. Create environment files:
   - Backend `.env` file with OpenAI API key
   - Frontend `.env` file with API URL

5. Start the services:
   - Backend: `uvicorn app.main:app --reload`
   - Frontend: `npm start`

### Speech-to-Text Features

TestMIND now supports voice input for a more natural interaction experience:

- **Real-time Voice Input**: Click the microphone button to start voice recognition
- **Audio File Upload**: Upload audio files (WAV, MP3, M4A, FLAC, OGG, WEBM) for transcription
- **Browser Compatibility**: Works with Chrome, Edge, Safari, and other modern browsers
- **Automatic Text Insertion**: Transcribed text is automatically added to the input field

**Note**: Speech recognition requires microphone permissions and works best in quiet environments.

For detailed setup instructions, see the [Backend README](backend/README.md) and [Frontend README](frontend/README.md).

## Team Members

<div align="center">
  <table>
    <tr>
      <td align="center">
        <a href="https://github.com/lms651">
          <img src="./banners/lori.png" width="100px;" alt="Team Member"/>
          <br />
          <sub><b>Lori Schmidt</b></sub>
        </a>
        <br />
        <sub>Team Lead</sub>
      </td>
      <td align="center">
        <a href="https://github.com/berkde">
          <img src="./banners/berk.png" width="100px;" alt="Berk Delibalta"/>
          <br />
          <sub><b>Berk Delibalta</b></sub>
        </a>
        <br />
        <sub>Lead Engineer and Architect</sub>
      </td>
      <td align="center">
        <a href="https://github.com/adamc95">
          <img src="./banners/adam.png" width="100px;" alt="Team Member"/>
          <br />
          <sub><b>Adam Cebulski</b></sub>
        </a>
        <br />
        <sub>QA Engineer</sub>
      </td>
      <td align="center">
        <a href="https://github.com/jxc1687">
          <img src="./banners/jiawei.png" width="100px;" alt="Team Member"/>
          <br />
          <sub><b>Jiawei Cheng</b></sub>
        </a>
        <br />
        <sub>Frontend Engineer</sub>
      </td>
    </tr>
  </table>
</div>

## Build Status

| Component | Status |
|-----------|--------|
| Backend   | [![Backend CI](https://github.com/berkde/testmind/actions/workflows/backend.yml/badge.svg)](https://github.com/berkde/testmind/actions/workflows/backend.yml) |
| Frontend  |  Coming Soon |

##  License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

##  Contact

For questions or feedback, please open an issue or contact the project maintainers.
