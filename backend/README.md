# TestMIND Backend

<div align="center">
  <img src="../banners/banner.png" alt="TestMIND Logo" width="200"/>

  [![Backend CI](https://github.com/berkde/testmind/actions/workflows/backend.yml/badge.svg)](https://github.com/berkde/testmind/actions/workflows/backend.yml)
  [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
  [![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
  [![FastAPI](https://img.shields.io/badge/FastAPI-0.68.0+-green.svg)](https://fastapi.tiangolo.com/)
  [![React](https://img.shields.io/badge/React-17.0.2+-blue.svg)](https://reactjs.org/)
  ![OpenAI](https://img.shields.io/badge/-OpenAI-412991?logo=OpenAI&logoColor=white&style=flat-square)
  ![LLaMA](https://img.shields.io/badge/-LLaMA-FF6F00?logo=Meta&logoColor=white)
  ![Render](https://img.shields.io/badge/-Render-46E3B7?logo=Render&logoColor=white)
</div>

---

## Project Description

**TestMIND Backend** is the FastAPI-powered backend for TestMIND, an AI-assisted tool designed to generate structured software test cases from natural language feature descriptions. It bridges the gap between human requirements and automated testing by combining advanced language models and rule-based logic.

- Processes natural language requirements
- Generates test cases using OpenAI GPT API
- Implements AllPairs test reduction
- Provides RESTful API endpoints for the frontend

---

## Features
- Generate positive, negative & edge test cases from natural language descriptions
- AllPairs test reduction to optimize test suite size
- API endpoints for test matrix generation and feedback
- CORS enabled for frontend-backend communication
- Deployed as a Web Service on Render

---

## Architecture

<details>
<summary>Click to expand</summary>

<pre>
graph TD
A[Natural Language Requirements] --> B[FastAPI Backend]
B --> C[OpenAI GPT API]
C --> D[Test Case Generator]
D --> E[React Frontend (UI)]
</pre>
</details>

---

## Project Structure

```
backend/
├── __init__.py
├── app/
│   ├── __init__.py
│   ├── api/
│   │   ├── __init__.py
│   │   └── endpoints.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── agent.py
│   │   ├── config.py
│   │   ├── testcase_generator.py
│   │   └── workflow.py
│   ├── main.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── error.py
│   │   ├── event.py
│   │   └── schemas.py
│   ├── services/
│   │   ├── __init__.py
│   │   └── handler.py
│   ├── utils/
│   │   ├── __init__.py
│   │   └── all_pairs.py
├── README.md
├── requirements.txt
└── tests/
    ├── __init__.py
    ├── conftest.py
    ├── demo_complex_matrix.py
    ├── demo_matrix.py
    ├── pytest.ini
    ├── README.md
    ├── test_generator.py
    ├── test_handler.py
    └── test_simple.py
```

---

## Getting Started

### Prerequisites
- Python 3.11 or higher
- pip (Python package installer)

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/berkde/testmind.git
   cd testmind/backend
   ```
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Environment Setup
1. Create a `.env` file in the backend directory with the following variables:
   ```
   OPENAI_API_KEY=your_openai_api_key
   # Add any other required secrets here
   ```

---

## Development

### Running the Server
Start the development server:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
The server will be available at http://localhost:8000.

### API Documentation
FastAPI automatically generates interactive API documentation:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---

## Deployment

This backend is deployed as a Render Web Service. For production, Render will set the `$PORT` environment variable automatically. Use this start command in Render:
```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

---

## API Endpoints
- Main endpoint: `POST /api/mind` (see [docs/api.md](docs/api.md) for full details)
- Health check: `GET /api/health`

---

## Testing

Run all tests:
```bash
python3 -m pytest tests/ -v
```
Run a specific test:
```bash
python3 -m pytest tests/test_handler.py::test_handler_basic_functionality -v
```

---

## Contributing
1. Create a feature branch from the development branch
2. Make your changes
3. Write or update tests
4. Submit a pull request to the development branch

---

## License
This project is licensed under the MIT License - see the [LICENSE](../LICENSE) file for details.