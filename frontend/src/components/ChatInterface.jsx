import React, { useState, useRef, useEffect } from 'react';
import { Send, Loader2, Brain, User, Copy, Download, FileText, Mic, MicOff, Upload } from 'lucide-react';
import { testMindAPI } from '../services/api';
import { exportToExcel, exportConversationToExcel } from '../utils/excelExport';
import ReactMarkdown from 'react-markdown';

const ChatInterface = () => {
  const [messages, setMessages] = useState([]);
  const [inputText, setInputText] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [copiedId, setCopiedId] = useState(null);
  const [isListening, setIsListening] = useState(false);
  const [transcript, setTranscript] = useState('');
  const [isTranscribing, setIsTranscribing] = useState(false);
  const messagesEndRef = useRef(null);
  const recognitionRef = useRef(null);
  const fileInputRef = useRef(null);
  // Remove TTS state and refs

  useEffect(() => {
    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
      const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
      recognitionRef.current = new SpeechRecognition();
      
      recognitionRef.current.continuous = true;
      recognitionRef.current.interimResults = true;
      recognitionRef.current.lang = 'en-US';
      
      let finalTranscriptLocal = '';
      
      recognitionRef.current.onstart = () => {
        setIsListening(true);
        setTranscript('');
        finalTranscriptLocal = '';
      };
      
      recognitionRef.current.onresult = (event) => {
        let interimTranscript = '';
        for (let i = event.resultIndex; i < event.results.length; i++) {
          const transcriptPiece = event.results[i][0].transcript;
          if (event.results[i].isFinal) {
            finalTranscriptLocal += transcriptPiece;
          } else {
            interimTranscript += transcriptPiece;
          }
        }
        setTranscript(finalTranscriptLocal + interimTranscript);
      };
      
      recognitionRef.current.onerror = (event) => {
        console.error('Speech recognition error:', event.error);
        setIsListening(false);
        setTranscript('');
      };
      
      recognitionRef.current.onend = () => {
        setIsListening(false);
        if (finalTranscriptLocal.trim()) {
          setTranscript('');
          sendMessageWithText(finalTranscriptLocal.trim());
        } else {
          setTranscript('');
        }
      };
    }
    
    return () => {
      if (recognitionRef.current) {
        recognitionRef.current.stop();
      }
    };
  }, []);

  const toggleListening = () => {
    if (!recognitionRef.current) {
      alert('Speech recognition is not supported in your browser. Please use Chrome, Edge, or Safari.');
      return;
    }
    
    if (isListening) {
      recognitionRef.current.stop();
    } else {
      recognitionRef.current.start();
    }
  };

  const handleAudioFileUpload = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    const allowedTypes = ['audio/wav', 'audio/mp3', 'audio/m4a', 'audio/flac', 'audio/ogg', 'audio/webm'];
    if (!allowedTypes.includes(file.type)) {
      alert('Please select a valid audio file (WAV, MP3, M4A, FLAC, OGG, or WEBM)');
      return;
    }

    if (file.size > 10 * 1024 * 1024) {
      alert('Audio file size must be less than 10MB');
      return;
    }

    setIsTranscribing(true);
    try {
      const result = await testMindAPI.transcribeAudio(file);
      
      if (result.status === 'success') {
        const newText = result.text;
        setInputText('');
        sendMessageWithText(newText);
      } else {
        alert(`Transcription failed: ${result.error_message}`);
      }
    } catch (error) {
      alert(`Error transcribing audio: ${error.message}`);
    } finally {
      setIsTranscribing(false);
      // Reset file input
      if (fileInputRef.current) {
        fileInputRef.current.value = '';
      }
    }
  };

  const triggerFileUpload = () => {
    fileInputRef.current?.click();
  };

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const sendMessageWithText = async (text) => {
    if (!text.trim() || isLoading) return;

    const userMessage = {
      id: Date.now(),
      type: 'user',
      content: text,
      timestamp: new Date().toLocaleTimeString(),
    };

    setMessages(prev => [...prev, userMessage]);
    setInputText('');
    setIsLoading(true);

    try {
      const response = await testMindAPI.sendMessage(text);
      const botMessage = {
        id: Date.now() + 1,
        type: 'bot',
        content: response,
        timestamp: new Date().toLocaleTimeString(),
      };
      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      const errorMessage = {
        id: Date.now() + 1,
        type: 'error',
        content: error.message,
        timestamp: new Date().toLocaleTimeString(),
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSendMessage = async () => {
    await sendMessageWithText(inputText);
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const copyToClipboard = async (text, id) => {
    try {
      await navigator.clipboard.writeText(text);
      setCopiedId(id);
      setTimeout(() => setCopiedId(null), 2000);
    } catch (err) {
      console.error('Failed to copy text: ', err);
    }
  };

  const handleExportMatrix = (matrixData, summary, recommendations, matrixStatistics) => {
    const timestamp = new Date().toISOString().slice(0, 19).replace(/:/g, '-');
    const filename = `testmind-matrix-${timestamp}.xlsx`;
    exportToExcel(matrixData, matrixStatistics, summary, recommendations, filename);
  };

  const handleExportConversation = () => {
    if (messages.length === 0) return;
    const timestamp = new Date().toISOString().slice(0, 19).replace(/:/g, '-');
    const filename = `testmind-conversation-${timestamp}.xlsx`;
    exportConversationToExcel(messages, filename);
  };

  const renderMessage = (message) => {
    const isBot = message.type === 'bot';
    const isError = message.type === 'error';
    const response = message.content;

    return (
      <div
        key={message.id}
        className={`flex gap-2 p-3 ${
          isBot ? 'bg-gray-50' : 'bg-white'
        } border-b border-gray-200`}
      >
        <div className={`w-6 h-6 rounded-full flex items-center justify-center flex-shrink-0 ${
          isBot ? 'bg-primary-100 text-primary-600' : 'bg-gray-100 text-gray-600'
        }`}>
          {isBot ? <Brain size={12} /> : <User size={12} />}
        </div>
        
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 mb-1">
            <span className="font-medium text-xs text-gray-700">
              {isBot ? 'TestMind AI' : 'You'}
            </span>
            <span className="text-xs text-gray-500">{message.timestamp}</span>
          </div>
          
          <div className="prose prose-xs max-w-none">
            {isError ? (
              <div className="text-red-600 bg-red-50 p-2 rounded text-sm">
                {response}
              </div>
            ) : isBot ? (
              <div>
                {response.status === 'conversation' && (
                  <div className="bg-blue-50 p-3 rounded mb-3 text-sm">
                    <ReactMarkdown>{response.response}</ReactMarkdown>
                  </div>
                )}
                
                {response.status === 'success' && (
                  <div className="space-y-3">
                    {response.summary && (
                      <div className="bg-green-50 p-3 rounded">
                        <h4 className="font-medium text-green-800 mb-1 text-sm">Summary</h4>
                        <ReactMarkdown className="text-sm">{response.summary}</ReactMarkdown>
                      </div>
                    )}
                    
                    {response.recommendations && (
                      <div className="bg-yellow-50 p-3 rounded">
                        <h4 className="font-medium text-yellow-800 mb-1 text-sm">Recommendations</h4>
                        <ReactMarkdown className="text-sm">{response.recommendations}</ReactMarkdown>
                      </div>
                    )}
                    
                    {response.matrix_data && Object.keys(response.matrix_data).length > 0 && (
                      <div className="bg-gray-50 p-3 rounded">
                        <div className="flex items-center justify-between mb-2">
                          <h4 className="font-medium text-gray-800 text-sm">Test Matrix</h4>
                          <div className="flex items-center gap-1">
                            <button
                              onClick={() => copyToClipboard(JSON.stringify(response.matrix_data, null, 2), message.id)}
                              className="text-gray-500 hover:text-gray-700 p-1 rounded"
                              title="Copy JSON"
                            >
                              {copiedId === message.id ? <Check size={14} /> : <Copy size={14} />}
                            </button>
                            <button
                              onClick={() => handleExportMatrix(response.matrix_data, response.summary, response.recommendations, response.matrix_statistics)}
                              className="text-green-600 hover:text-green-700 p-1 rounded"
                              title="Export to Excel"
                            >
                              <Download size={14} />
                            </button>
                          </div>
                        </div>
                        <MatrixDisplay matrixData={response.matrix_data} matrixStatistics={response.matrix_statistics} />
                      </div>
                    )}
                  </div>
                )}
                
                {response.status === 'error' && (
                  <div className="text-red-600 bg-red-50 p-2 rounded text-sm">
                    {response.error_message || 'An error occurred'}
                  </div>
                )}
              </div>
            ) : (
              <div className="text-gray-800 text-sm">
                <ReactMarkdown>{response}</ReactMarkdown>
              </div>
            )}
          </div>
        </div>
      </div>
    );
  };

  // Remove TTS useEffect

  return (
    <div className="flex flex-col h-full max-h-full">
      <div className="flex-1 overflow-y-auto pb-4 min-h-0">
        {messages.length === 0 ? (
          <div className="flex items-center justify-center h-full text-gray-500">
            <div className="text-center">
              <Brain size={32} className="mx-auto mb-3 text-gray-300" />
              <h3 className="text-base font-medium mb-1">Welcome to TestMind</h3>
              <p className="text-xs">
                Start a conversation or ask me to generate a test matrix for your software transitions and personas.
              </p>
            </div>
          </div>
        ) : (
          <>
            {messages.length > 0 && (
              <div className="sticky top-0 bg-white border-b border-gray-200 p-2 z-10">
                <div className="flex items-center justify-between">
                  <span className="text-xs text-gray-600">
                    {messages.length} message{messages.length !== 1 ? 's' : ''}
                  </span>
                  <button
                    onClick={handleExportConversation}
                    className="flex items-center gap-1 text-xs text-blue-600 hover:text-blue-700 px-2 py-1 rounded hover:bg-blue-50"
                    title="Export conversation to Excel"
                  >
                    <FileText size={12} />
                    Export Chat
                  </button>
                </div>
              </div>
            )}
            {messages.map(renderMessage)}
          </>
        )}
        
        {isLoading && (
          <div className="flex gap-2 p-3 bg-gray-50 border-b border-gray-200">
            <div className="w-6 h-6 rounded-full bg-primary-100 text-primary-600 flex items-center justify-center flex-shrink-0">
              <Brain size={12} />
            </div>
            <div className="flex-1">
              <div className="flex items-center gap-2 mb-1">
                <span className="font-medium text-xs text-gray-700">TestMind AI</span>
              </div>
              <div className="flex items-center gap-2 text-gray-500">
                <Loader2 size={12} className="animate-spin" />
                <span className="text-xs">Processing your request...</span>
              </div>
            </div>
          </div>
        )}
        
        <div ref={messagesEndRef} />
      </div>
      
      <div className="border-t border-gray-200 p-3 bg-white shadow-lg">
        {/* Remove TTS toggle button */}
        {/* Speech transcript indicator */}
        {isListening && (
          <div className="mb-2 p-2 bg-blue-50 border border-blue-200 rounded text-sm">
            <div className="flex items-center gap-2 text-blue-700">
              <div className="w-2 h-2 bg-red-500 rounded-full animate-pulse"></div>
              <span className="font-medium">Listening...</span>
            </div>
            {transcript && (
              <div className="mt-1 text-blue-800 italic">
                "{transcript}"
              </div>
            )}
            <div className="mt-1 text-xs text-blue-600">
              Message will be sent automatically when you stop speaking
            </div>
          </div>
        )}

        {isTranscribing && (
          <div className="mb-2 p-2 bg-green-50 border border-green-200 rounded text-sm">
            <div className="flex items-center gap-2 text-green-700">
              <Loader2 size={12} className="animate-spin" />
              <span className="font-medium">Transcribing audio...</span>
            </div>
            <div className="mt-1 text-xs text-green-600">
              Message will be sent automatically after transcription
            </div>
          </div>
        )}
        
        <div className="flex gap-2">
          <textarea
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Type your message here... (Press Enter to send, Shift+Enter for new line)"
            className="input-field flex-1 resize-none text-sm"
            rows={2}
            disabled={isLoading}
          />
          <div className="flex flex-col gap-1 self-end">
            <button
              onClick={toggleListening}
              disabled={isLoading || isTranscribing}
              className={`p-2 rounded transition-colors ${
                isListening 
                  ? 'bg-red-100 text-red-600 hover:bg-red-200' 
                  : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
              } disabled:opacity-50 disabled:cursor-not-allowed`}
              title={isListening ? 'Stop listening' : 'Start voice input'}
            >
              {isListening ? <MicOff size={14} /> : <Mic size={14} />}
            </button>
            <button
              onClick={triggerFileUpload}
              disabled={isLoading || isTranscribing}
              className="p-2 rounded bg-gray-100 text-gray-600 hover:bg-gray-200 disabled:opacity-50 disabled:cursor-not-allowed"
              title="Upload audio file"
            >
              {isTranscribing ? <Loader2 size={14} className="animate-spin" /> : <Upload size={14} />}
            </button>
            <button
              onClick={handleSendMessage}
              disabled={!inputText.trim() || isLoading}
              className="btn-primary disabled:opacity-50 disabled:cursor-not-allowed px-3 py-2"
              title="Send message"
            >
              <Send size={14} />
            </button>
          </div>
        </div>

        <input
          ref={fileInputRef}
          type="file"
          accept="audio/*"
          onChange={handleAudioFileUpload}
          style={{ display: 'none' }}
        />
      </div>
    </div>
  );
};

const MatrixDisplay = ({ matrixData, matrixStatistics }) => {
  const transitions = Object.keys(matrixData);
  const personas = new Set();
  
  transitions.forEach(transition => {
    Object.keys(matrixData[transition]).forEach(persona => {
      personas.add(persona);
    });
  });
  
  const personaArray = Array.from(personas);

  return (
    <div>
      {/* Statistics Section */}
      {matrixStatistics && Object.keys(matrixStatistics).length > 0 && (
        <div className="mb-4 p-3 bg-blue-50 rounded-lg border border-blue-200">
          <h5 className="font-medium text-blue-900 mb-2 text-sm">Matrix Statistics</h5>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-3 text-xs">
            <div className="text-center">
              <div className="font-semibold text-blue-800">{matrixStatistics.total_combinations || 0}</div>
              <div className="text-blue-600">Total Combinations</div>
            </div>
            <div className="text-center">
              <div className="font-semibold text-green-800">{matrixStatistics.essential_combinations || 0}</div>
              <div className="text-green-600">Essential (Green)</div>
            </div>
            <div className="text-center">
              <div className="font-semibold text-yellow-800">{matrixStatistics.optional_combinations || 0}</div>
              <div className="text-yellow-600">Redundant (Yellow)</div>
            </div>
            <div className="text-center">
              <div className="font-semibold text-red-800">{matrixStatistics.prohibited_combinations || 0}</div>
              <div className="text-red-600">Prohibited (Red)</div>
            </div>
          </div>
        </div>
      )}

      {/* Matrix Table */}
      <div className="overflow-x-auto">
        <table className="min-w-full border border-gray-300">
          <thead>
            <tr className="bg-gray-100">
              <th className="border border-gray-300 px-3 py-2 text-left font-medium">Transition</th>
              {personaArray.map(persona => (
                <th key={persona} className="border border-gray-300 px-3 py-2 text-left font-medium">
                  {persona}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {transitions.map(transition => (
              <tr key={transition}>
                <td className="border border-gray-300 px-3 py-2 font-medium bg-gray-50">
                  {transition}
                </td>
                {personaArray.map(persona => {
                  const data = matrixData[transition][persona];
                  const status = data?.status || 'Unknown';
                  const statusColor = {
                    'Essential': 'bg-green-100 text-green-800',
                    'Optional': 'bg-yellow-100 text-yellow-800',
                    'Prohibited': 'bg-red-100 text-red-800',
                    'Unknown': 'bg-gray-100 text-gray-800'
                  }[status] || 'bg-gray-100 text-gray-800';
                  
                  return (
                    <td key={persona} className="border border-gray-300 px-3 py-2">
                      <div className="flex items-center gap-2">
                        <span className={`px-2 py-1 rounded text-xs font-medium ${statusColor}`}>
                          {status}
                        </span>
                        {data?.id && (
                          <span className="text-xs text-gray-500">({data.id})</span>
                        )}
                      </div>
                    </td>
                  );
                })}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default ChatInterface; 