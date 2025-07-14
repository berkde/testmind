import React from 'react';
import ChatInterface from '../components/ChatInterface';

const Home = () => {
  return (
    <div className="flex-1 flex flex-col">
      <main className="h-[90vh] overflow-hidden">
        <ChatInterface />
      </main>
    </div>
  );
};

export default Home;
