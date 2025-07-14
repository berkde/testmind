import React, { useState, useEffect } from 'react';
import { Wifi, WifiOff, AlertCircle } from 'lucide-react';
import { testMindAPI } from '../services/api';

const ConnectionStatus = () => {
  const [isConnected, setIsConnected] = useState(null);
  const [isChecking, setIsChecking] = useState(true);
  const [errorMessage, setErrorMessage] = useState('');

  useEffect(() => {
    const checkConnection = async () => {
      try {
        console.log('Checking backend connection...');
        const connected = await testMindAPI.checkHealth();
        console.log('Backend connection result:', connected);
        setIsConnected(connected);
        setErrorMessage('');
      } catch (error) {
        console.error('Backend connection error:', error);
        setIsConnected(false);
        setErrorMessage(error.message);
      } finally {
        setIsChecking(false);
      }
    };

    checkConnection();
    
    // Check connection every 30 seconds
    const interval = setInterval(checkConnection, 30000);
    
    return () => clearInterval(interval);
  }, []);

  if (isChecking) {
    return (
      <div className="flex items-center gap-2 text-gray-500 text-sm">
        <div className="w-3 h-3 bg-gray-300 rounded-full animate-pulse"></div>
        <span>Checking connection...</span>
      </div>
    );
  }

  if (isConnected === null) {
    return null;
  }

  return (
    <div className={`flex items-center gap-2 text-sm ${
      isConnected ? 'text-green-600' : 'text-red-600'
    }`}>
      {isConnected ? (
        <>
          <Wifi size={14} />
          <span>Connected to TestMind</span>
        </>
      ) : (
        <>
          <WifiOff size={14} />
          <span>Backend unavailable</span>
          {errorMessage && (
            <span className="text-xs text-gray-500">({errorMessage})</span>
          )}
        </>
      )}
    </div>
  );
};

export default ConnectionStatus; 