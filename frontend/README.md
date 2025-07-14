# TestMind Frontend

A modern React-based frontend for the TestMind AI-powered test case generation tool.

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
