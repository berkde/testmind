import React from 'react';
import { Brain, MessageSquare, Table, Users, Zap, Shield } from 'lucide-react';
import { Link } from 'react-router-dom';
// import landingBg from '../assets/landing-bg.jpg';

const features = [
  {
    icon: Brain,
    title: 'AI-Powered Analysis',
    description: 'Uses advanced language models to understand your software requirements and generate comprehensive test cases.'
  },
  {
    icon: Table,
    title: 'Structured Test Matrices',
    description: 'Creates organized test matrices that map transitions between states for different user personas.'
  },
  {
    icon: Users,
    title: 'Persona-Based Testing',
    description: 'Generates test scenarios tailored to different user roles and access levels.'
  },
  {
    icon: Zap,
    title: 'Real-time Generation',
    description: 'Instantly generates test matrices and provides recommendations for improving test coverage.'
  },
  {
    icon: Shield,
    title: 'Quality Assurance',
    description: 'Ensures comprehensive test coverage with validation and error handling recommendations.'
  }
];

const Landing = () => {
  return (
    <div className="relative min-h-10 min-w-10 flex flex-col items-center justify-center px-4 py-3 overflow-hidden bg-gradient-to-br from-indigo-200 via-blue-300 to-slate-400">
      {/* Overlay for better contrast */}
      <div className="absolute inset-0 bg-slate-900/20 pointer-events-none z-10" />
      <div className="relative z-20 max-w-2xl w-full text-center mb-12">
        <div className="flex justify-center mb-4">
          <img
            src="/banner.png"
            alt="TestMind Emblem"
            className="w-24 h-24 rounded-lg shadow-lg object-contain bg-white/80"
            style={{ border: '2px solid #fff' }}
          />
        </div>
        <h1 className="text-4xl md:text-5xl font-bold text-white mb-4 drop-shadow-lg">Welcome to TestMind</h1>
        <p className="text-lg text-gray-200 mb-6 drop-shadow">
          TestMind is your AI-powered assistant for generating comprehensive test matrices and scenarios for your software projects. Let AI do the heavy lifting for your QA process!
        </p>
        <Link to="/chat" className="btn-primary text-lg px-8 py-3 inline-flex items-center gap-2">
          <MessageSquare size={20} />
          Get Started
        </Link>
      </div>
      <div className="relative z-20 max-w-4xl w-full grid md:grid-cols-2 gap-8">
        {features.map((feature, idx) => (
          <div key={idx} className="card flex items-start gap-4 bg-white/80 backdrop-blur-md">
            <feature.icon size={32} className="text-primary-600 flex-shrink-0" />
            <div>
              <h3 className="font-semibold text-gray-900 mb-1">{feature.title}</h3>
              <p className="text-gray-600 text-sm">{feature.description}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Landing; 