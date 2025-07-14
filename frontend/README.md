# TestMIND Frontend

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

## Table of Contents

- [Project Description](#project-description)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Development](#development)
- [Building for Production](#building-for-production)
- [Usage](#usage)
  - [Getting Started](#getting-started)
  - [Example Interactions](#example-interactions)
  - [Understanding the Response](#understanding-the-response)
  - [Matrix Display](#matrix-display)
- [Project Structure](#project-structure)
- [Technologies Used](#technologies-used)
- [Troubleshooting](#troubleshooting)
  - [Connection Issues](#connection-issues)
  - [Build Issues](#build-issues)
  - [Performance Issues](#performance-issues)
- [Contributing](#contributing)

## Project Description

**TestMIND** (Test Management, Integration, and Natural Development) is an AI-assisted tool designed to generate structured software test cases from natural language feature descriptions. It bridges the gap between human requirements and automated testing by combining Natural Language Processing (NLP) and rule-based logic.

Our mission is to streamline the software testing process by automatically generating comprehensive test suites from plain English requirements, saving development teams valuable time and ensuring thorough test coverage.


## Features

- **Chat Interface**: Natural language interaction with the TestMind AI
- **Real-time Matrix Display**: Visual representation of generated test matrices
- **Conversation Support**: Handle both casual conversation and structured test generation
- **Connection Status**: Real-time backend connectivity monitoring
- **Responsive Design**: Works on desktop and mobile devices
- **Modern UI**: Built with Tailwind CSS and Lucide React icons

## Prerequisites

- Node.js 18+ 
- npm or yarn
- TestMind backend running on `http://localhost:8000`

## Installation

1. Install dependencies:
```bash
npm install --legacy-peer-deps
```

2. Create environment file (optional):
```bash
cp .env.example .env
```

3. Configure the API URL in `.env` (defaults to `http://localhost:8000`):
```
VITE_API_URL=http://localhost:8000
```

## Development

Start the development server:
```bash
npm run dev
```

The frontend will be available at `http://localhost:5173`

## Building for Production

Build the application:
```bash
npm run build
```

Preview the production build:
```bash
npm run preview
```

## Usage

### Getting Started

1. **Start the Backend**: Ensure the TestMind backend is running on port 8000
2. **Open the Frontend**: Navigate to `http://localhost:5173`
3. **Check Connection**: The header shows the connection status to the backend
4. **Start Chatting**: Type your message in the chat interface

### Example Interactions

#### Basic Test Matrix Request
```
Generate a test matrix for login to dashboard transitions for admin and guest users.
```

#### Complex Workflow Testing
```
Create test cases for user registration, email verification, and profile setup workflows.
```

#### Multi-Persona Scenarios
```
Test the checkout process for customers, managers, and administrators with different permissions.
```

### Understanding the Response

The AI will respond with different types of content:

- **Conversation**: General chat responses when not generating test matrices
- **Success**: Generated test matrices with:
  - Summary of the test cases
  - Recommendations for improvement
  - Visual matrix table showing transitions and personas
- **Error**: Error messages with suggestions for fixing the request

### Matrix Display

The generated test matrix shows:
- **Transitions**: State changes (e.g., "login→dashboard")
- **Personas**: User roles (e.g., "admin", "guest", "user")
- **Status**: Test status indicators (Green, Yellow, Red)
- **Test IDs**: Unique identifiers for each test case

## Project Structure

```
src/
├── components/
│   ├── ChatInterface.jsx    # Main chat component
│   ├── ConnectionStatus.jsx # Backend connectivity indicator
│   └── Header.jsx          # Navigation header
├── pages/
│   ├── Home.jsx            # Chat interface page
│   └── About.jsx           # Information page
├── services/
│   └── api.js              # Backend API communication
└── App.jsx                 # Main application component
```

## Technologies Used

- **React 18**: UI framework
- **React Router**: Client-side routing
- **Tailwind CSS**: Utility-first CSS framework
- **Lucide React**: Icon library
- **Axios**: HTTP client for API calls
- **React Markdown**: Markdown rendering
- **Vite**: Build tool and dev server

## Troubleshooting

### Connection Issues
- Ensure the backend is running on port 8000
- Check the connection status indicator in the header
- Verify the API URL in your environment configuration

### Build Issues
- Use `--legacy-peer-deps` flag when installing dependencies
- Clear node_modules and reinstall if dependency conflicts occur

### Performance Issues
- The frontend is optimized for modern browsers
- Large test matrices may take time to render
- Consider breaking down complex requests into smaller parts

## Contributing

1. Create a feature branch from the development branch
2. Make your changes
3. Write or update tests
4. Submit a pull request to the development branch
