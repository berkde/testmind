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

This is the React-based frontend application for TestMIND, an AI-assisted tool designed to generate structured software test cases from natural language feature descriptions.

## Table of Contents

- [Overview](#overview)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Environment Setup](#environment-setup)
- [Development](#development)
  - [Running the Application](#running-the-application)
  - [Building for Production](#building-for-production)
- [Testing](#testing)
- [Deployment](#deployment)
- [Contributing](#contributing)

## Overview

The TestMIND frontend is a React-based web application that provides a user-friendly interface for:

- Inputting natural language requirements
- Viewing and managing generated test cases
- Configuring test generation parameters
- Exporting test cases in various formats

**Note:** The React frontend is currently in early development stage.

## Technology Stack

- **React**: Frontend library for building user interfaces
- **React Router**: For navigation
- **Axios**: For API requests
- **CSS Modules/Styled Components**: For styling

**Note:** While Node.js and npm/yarn are used as development tools, the frontend application itself is built with React, not Node.js.

## Project Structure

```
frontend/
├── public/                # Static files
├── src/                   # Source code
│   ├── components/        # Reusable UI components
│   ├── pages/             # Page components
│   ├── services/          # API services
│   ├── utils/             # Utility functions
│   ├── App.jsx            # Main application component
│   └── main.jsx           # Application entry point
├── package.json           # Project dependencies and scripts
├── vite.config.js         # Vite configuration
├── eslint.config.js       # ESLint configuration
├── index.html             # HTML template
└── README.md              # This file
```

## Getting Started

### Prerequisites

- Node.js 14.x or higher (required for development tools, not for the frontend application itself)
- npm 6.x or higher (or yarn) (package manager for installing dependencies)

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/berkde/testmind.git
   cd testmind/frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   # or
   yarn install
   ```

### Environment Setup

1. Create a `.env` file in the frontend directory with the following variables:
   ```
   REACT_APP_API_URL=http://localhost:8000/api/v1
   ```

## Development

### Running the Application

Start the React development server:

```bash
npm run dev
# or
yarn dev
```

This will start the React application in development mode. The application will be available at http://localhost:5173 in your web browser.

### Building for Production

Create a production-ready build of the React application:

```bash
npm run build
# or
yarn build
```

This will create optimized production files of the React application. The build artifacts will be stored in the `build/` directory and can be served by any static file server.

## Testing

Run React component tests:

```bash
npm test
# or
yarn test
```

This will run the test suite for React components and other frontend code using Jest and React Testing Library.

## Deployment

The React application is configured to be deployed using GitHub Actions. The workflow is defined in `.github/workflows/frontend.yml`.

For manual deployment of the React application:

1. Build the React application:

   ```bash
   npm run build
   # or
   yarn build
   ```

2. Deploy the contents of the `build` directory to your web server or static file hosting service (like Netlify, Vercel, or AWS S3).

## Contributing

1. Create a feature branch from the development branch
2. Make your changes
3. Write or update tests
4. Submit a pull request to the development branch
