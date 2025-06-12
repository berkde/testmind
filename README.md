# TestMIND 

<div align="center">
  <img src="banners/banner.png" alt="TestMIND Logo" width="200"/>

  [![Backend CI](https://github.com/berkde/testmind/actions/workflows/backend.yml/badge.svg)](https://github.com/berkde/testmind/actions/workflows/backend.yml)
  [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
  [![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
  [![FastAPI](https://img.shields.io/badge/FastAPI-0.68.0+-green.svg)](https://fastapi.tiangolo.com/)
  [![React](https://img.shields.io/badge/React-17.0.2+-blue.svg)](https://reactjs.org/)
  ![Hugging Face](https://img.shields.io/badge/-Hugging%20Face-FDEE21?logo=HuggingFace&logoColor=black)
  ![OpenAI](https://img.shields.io/badge/-OpenAI-412991?logo=OpenAI&logoColor=white&style=flat-square)


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

---

##  Tech Stack

| Layer       | Tech                      |
|------------|---------------------------|
| Backend    | Python, FastAPI, HuggingFace Transformers, OpenAI |
| Frontend   | React, TypeScript         |
| ML Models  | Custom NLP Pipelines via HuggingFace |
| API Access | OpenAI GPT API            |
| Testing    | Pytest, React Testing Library |
| CI/CD      | GitHub Actions            |

---

##  Architecture

<details>
<summary>Click to expand</summary>

<pre>
graph TD
A[Natural Language Requirements] --> B[FastAPI Backend]
B --> C[HuggingFace NLP Pipeline]
C --> D[OpenAI GPT API]
B --> E[Test Case Generator]
D --> G[React Frontend (UI)]
</pre> </details>


## Repository Structure


<details>
<summary>Click to expand</summary>

<pre>
testmind/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # FastAPI app entry point
│   │   ├── api/                 # Route handlers
│   │   │   ├── __init__.py
│   │   │   └── endpoints.py
│   │   ├── core/                # Configs, OpenAI/HF setup
│   │   │   └── config.py
│   │   ├── models/              # Pydantic models / data schemas
│   │   │   └── schemas.py
│   │   ├── services/            # Business logic, HuggingFace + OpenAI wrappers
│   │   │   └── test_generator.py
│   │   ├── utils/               # Utilities and helpers
│   │   │   └── all_pairs.py
│   ├── tests/                   # Backend unit tests
│   │   └── test_generator.py
│   ├── requirements.txt
│   └── README.md
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── App.tsx
│   │   └── index.tsx
│   ├── .env
│   ├── package.json
│   └── README.md
│
├── .github/
│   └── workflows/
│       └── backend.yml          # GitHub CI workflow
│
├── README.md                    # Project overview
├── .gitignore
└── LICENSE
</pre> </details>

## Getting Started

### Prerequisites

- Python 3.13.3 or higher
- Node.js 14.x or higher
- OpenAI API key
- HuggingFace API key (optional)

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
        <a href="#">
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
