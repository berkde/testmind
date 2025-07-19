# TestMIND Frontend

<div align="center">
  <img src="../banners/banner.png" alt="TestMIND Logo" width="200"/>

  [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
  ![JavaScript](https://img.shields.io/badge/JavaScript-ES6+-F7DF1E?logo=javascript&logoColor=black)
  [![React](https://img.shields.io/badge/React-18.0.0+-blue.svg)](https://reactjs.org/)
  ![OpenAI](https://img.shields.io/badge/-OpenAI-412991?logo=OpenAI&logoColor=white&style=flat-square)
  ![Render](https://img.shields.io/badge/-Render-46E3B7?logo=Render&logoColor=white)
</div>

---

## Project Description

**TestMIND Frontend** is the React (Vite) UI for TestMIND, an AI-powered tool for generating structured software test cases from natural language requirements. It provides a modern, interactive chat interface for users to describe their software, request test matrices, and review results.

- Conversational UI for test matrix generation
- Real-time matrix display and export
- Voice input via Google Web Speech API
- Responsive, modern design

---

## Features
- Chat interface for natural language interaction
- Real-time matrix and summary display
- Voice input (speech-to-text) using Google Web Speech API
- Export to Excel and copy matrix data
- Connection status indicator for backend API
- Responsive design for desktop and mobile

---

## Architecture
- User interacts via browser (text or voice input)
- Voice input is transcribed using Google Web Speech API
- React frontend sends API requests to the FastAPI backend (on Render)
- Backend communicates with OpenAI GPT API and returns test matrices

---

## Getting Started

### Prerequisites
- Node.js 18+
- npm or yarn
- TestMIND backend running (locally or on Render)

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/berkde/testmind.git
   cd testmind/frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Set up environment variable for backend API:
   - Create a `.env` file in `frontend/` with:
     ```
     VITE_API_URL=https://your-backend-service.onrender.com
     ```
4. Run locally:
   ```bash
   npm run dev
   ```

---

## Usage
- Start the backend (locally or ensure the Render backend is running)
- Start the frontend (`npm run dev`)
- Open [http://localhost:5173](http://localhost:5173) in your browser
- Describe your software and request a test matrix
- Use the voice input button for speech-to-text (requires Chrome or compatible browser)
- Export or copy the generated matrix as needed

---

## Deployment
- Deployed as a Static Site on Render
- Build command: `npm run build`
- Publish directory: `dist`
- Set `VITE_API_URL` in Render environment variables to your backend Render URL

---

## Project Structure
```
frontend/
├── public/
│   └── banner.png
├── src/
│   ├── assets/
│   ├── components/
│   │   ├── ChatInterface.jsx
│   │   ├── ConnectionStatus.jsx
│   │   └── Header.jsx
│   ├── pages/
│   │   ├── Home.jsx
│   │   ├── About.jsx
│   │   ├── Contact.jsx
│   │   └── Landing.jsx
│   ├── services/
│   │   └── api.js
│   ├── utils/
│   │   └── excelExport.js
│   ├── App.jsx
│   ├── main.jsx
│   └── index.css
├── package.json
├── README.md
└── ...
```

---

## Troubleshooting
- **Connection Issues:** Ensure the backend is running and `VITE_API_URL` is set correctly
- **Voice Input Issues:** Use Chrome or a browser supporting the Web Speech API
- **Build Issues:** Clear `node_modules` and reinstall dependencies if you encounter errors

---

## Contributing
1. Create a feature branch from the development branch
2. Make your changes
3. Write or update tests
4. Submit a pull request to the development branch

---

## License
This project is licensed under the MIT License - see the [LICENSE](../LICENSE) file for details.
