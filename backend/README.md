# TestMIND Backend

<div align="center">
  <img src="../banners/banner.png" alt="TestMIND Logo" width="200"/>

  [![Backend CI](https://github.com/berkde/testmind/actions/workflows/backend.yml/badge.svg)](https://github.com/berkde/testmind/actions/workflows/backend.yml)
  [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
  [![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
  [![FastAPI](https://img.shields.io/badge/FastAPI-0.68.0+-green.svg)](https://fastapi.tiangolo.com/)
  [![React](https://img.shields.io/badge/React-17.0.2+-blue.svg)](https://reactjs.org/)
  ![Hugging Face](https://img.shields.io/badge/-Hugging%20Face-FDEE21?logo=HuggingFace&logoColor=black)
  ![OpenAI](https://img.shields.io/badge/-OpenAI-412991?logo=OpenAI&logoColor=white&style=flat-square)

</div>


This is the backend service for TestMIND, an AI-assisted tool designed to generate structured software test cases from natural language feature descriptions.

## Table of Contents

- [Overview](#overview)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Environment Setup](#environment-setup)
- [Development](#development)
  - [Running the Server](#running-the-server)
  - [API Documentation](#api-documentation)
- [Testing](#testing)
- [Deployment](#deployment)
- [Contributing](#contributing)

## Overview

The TestMIND backend is responsible for:
- Processing natural language requirements
- Generating test cases using NLP and AI models
- Implementing AllPairs test reduction
- Providing RESTful API endpoints for the frontend

## Technology Stack

- **Python**: Main programming language
- **FastAPI**: Web framework for building APIs
- **HuggingFace Transformers**: NLP models and pipelines
- **OpenAI**: GPT API integration for advanced language processing
- **Pytest**: Testing framework

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
   # API Keys
   OPENAI_API_KEY=your_openai_api_key
   HUGGINGFACE_API_KEY=your_huggingface_api_key
   
   # App Configuration
   DEBUG=True
   API_PREFIX=/api/v1
   ```

## Development

### Running the Server

Start the development server:

```bash
uvicorn app.main:app --reload
```

The server will be available at http://localhost:8000.

### API Documentation

FastAPI automatically generates interactive API documentation:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Testing

Run tests using pytest:

```bash
pytest
```

For more verbose output:

```bash
pytest -v
```

To run specific tests:

```bash
pytest tests/test_generator.py
```

## Deployment

The application is configured to be deployed using GitHub Actions. The workflow is defined in `.github/workflows/backend.yml`.

For manual deployment:

1. Build the Docker image:
   ```bash
   docker build -t testmind-backend .
   ```

2. Run the container:
   ```bash
   docker run -p 8000:8000 testmind-backend
   ```

## Contributing

1. Create a feature branch from the development branch
2. Make your changes
3. Write or update tests
4. Submit a pull request to the development branch