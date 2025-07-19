import React from 'react';
import { Brain, MessageSquare, Table, Users, ArrowRight, CheckCircle, Zap, Shield, BarChart3 } from 'lucide-react';

const About = () => {
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
      icon: MessageSquare,
      title: 'Conversational Interface',
      description: 'Natural language interaction that can handle both casual conversation and structured test generation requests.'
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

  const examples = [
    {
      title: 'Basic Test Matrix Request',
      example: 'Generate a test matrix for login to dashboard transitions for admin and guest users.',
      description: 'Simple state transition testing with multiple user roles.'
    },
    {
      title: 'Complex Workflow Testing',
      example: 'Create test cases for user registration, email verification, and profile setup workflows.',
      description: 'Multi-step process testing with various user scenarios.'
    },
    {
      title: 'Multi-Persona Scenarios',
      example: 'Test the checkout process for customers, managers, and administrators with different permissions.',
      description: 'Role-based access control testing across different user types.'
    }
  ];

  const benefits = [
    'Reduces manual test case creation time by 80%',
    'Ensures comprehensive coverage of user scenarios',
    'Identifies edge cases and potential issues',
    'Provides actionable recommendations for improvement',
    'Supports multiple user roles and permissions',
    'Generates exportable test matrices for team collaboration'
  ];

  return (
    <div className="relative bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50 overflow-hidden">
      {/* Animated background elements */}
      <div className="absolute inset-0">
        <div className="absolute top-0 left-0 w-72 h-72 bg-primary-200 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-blob"></div>
        <div className="absolute top-0 right-0 w-72 h-72 bg-purple-200 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-blob animation-delay-2000"></div>
        <div className="absolute -bottom-8 left-20 w-72 h-72 bg-pink-200 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-blob animation-delay-4000"></div>
      </div>
      
      {/* Grid pattern overlay */}
      <div className="absolute inset-0 opacity-30" style={{
        backgroundImage: `url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%239C92AC' fill-opacity='0.05'%3E%3Ccircle cx='30' cy='30' r='1'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E")`
      }}></div>
      
      <div className="relative max-w-6xl mx-auto px-4 py-12">
        {/* Hero Section */}
        <div className="text-center mb-16">
          <div className="flex justify-center mb-8">
            <img
              src="/banner.png"
              alt="TestMind Emblem"
              className="w-24 h-24 rounded-lg shadow-lg object-contain bg-white/80"
              style={{ border: '2px solid #fff' }}
            />
          </div>
          <h1 className="text-4xl md:text-5xl font-bold text-gray-900 mb-6">About TestMind</h1>
          <p className="text-xl text-gray-600 max-w-4xl mx-auto leading-relaxed">
            TestMind is an AI-assisted tool that converts transition states, personas, and requirements 
            from specific applications into structured software test combination tables using LLM-powered AI agents.
          </p>
        </div>

        <div className="mb-20">
          <h2 className="text-3xl md:text-4xl font-bold text-gray-900 text-center mb-12">Key Features</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {features.map((feature, index) => {
              const Icon = feature.icon;
              return (
                <div key={index} className="bg-white rounded-xl shadow-md hover:shadow-xl transition-all duration-300 p-8 border border-gray-100">
                  <div className="w-16 h-16 bg-primary-100 rounded-xl flex items-center justify-center mb-6">
                    <Icon size={32} className="text-primary-600" />
                  </div>
                  <h3 className="text-xl font-semibold text-gray-900 mb-4">{feature.title}</h3>
                  <p className="text-gray-600 leading-relaxed">{feature.description}</p>
                </div>
              );
            })}
          </div>
        </div>

        <div className="bg-white rounded-xl shadow-md border border-gray-100 p-8 md:p-12 mb-16">
          <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-12 text-center">How to Use TestMind</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="text-center">
              <div className="w-20 h-20 bg-primary-600 text-white rounded-full flex items-center justify-center text-2xl font-bold mx-auto mb-6 shadow-lg">
                1
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-4">Start a Conversation</h3>
              <p className="text-gray-600 leading-relaxed">
                Begin by describing your software application, its user flows, and the personas that will interact with it.
              </p>
            </div>
            
            <div className="text-center">
              <div className="w-20 h-20 bg-primary-600 text-white rounded-full flex items-center justify-center text-2xl font-bold mx-auto mb-6 shadow-lg">
                2
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-4">Request Test Matrix Generation</h3>
              <p className="text-gray-600 leading-relaxed">
                Ask TestMind to generate a test matrix for specific transitions and personas. Be specific about the states and user roles.
              </p>
            </div>
            
            <div className="text-center">
              <div className="w-20 h-20 bg-primary-600 text-white rounded-full flex items-center justify-center text-2xl font-bold mx-auto mb-6 shadow-lg">
                3
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-4">Review and Export</h3>
              <p className="text-gray-600 leading-relaxed">
                Review the generated test matrix and recommendations. Export to Excel or copy the data for use in your testing tools.
              </p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-xl shadow-md border border-gray-100 p-8 md:p-12 mb-16">
          <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-12 text-center">Why Choose TestMind?</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {benefits.map((benefit, index) => (
              <div key={index} className="flex items-start gap-4 p-4 bg-gray-50 rounded-lg">
                <CheckCircle size={24} className="text-green-500 mt-0.5 flex-shrink-0" />
                <span className="text-gray-700 font-medium">{benefit}</span>
              </div>
            ))}
          </div>
        </div>

        <div className="bg-white rounded-xl shadow-md border border-gray-100 p-8 md:p-12 mb-16">
          <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-12 text-center">Example Requests</h2>
          <div className="space-y-8">
            {examples.map((example, index) => (
              <div key={index} className="border border-gray-200 rounded-xl p-8 hover:shadow-lg transition-all duration-300 bg-gray-50">
                <h3 className="text-xl font-semibold text-gray-900 mb-4">{example.title}</h3>
                <div className="bg-white p-6 rounded-lg border-l-4 border-primary-500 mb-4 shadow-sm">
                  <p className="text-gray-700 font-mono text-sm leading-relaxed">{example.example}</p>
                </div>
                <p className="text-gray-600 text-sm leading-relaxed">{example.description}</p>
              </div>
            ))}
          </div>
        </div>

        <div className="bg-white rounded-xl shadow-md border border-gray-100 p-8 md:p-12 mb-16">
          <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-12 text-center">TestMind in Action</h2>
          <div className="space-y-12">
            <div className="text-center">
              <h3 className="text-xl font-semibold text-gray-900 mb-6">Interface Overview</h3>
              <img 
                src="/1.png"
                alt="TestMind Interface Screenshot 1" 
                className="w-full max-w-6xl mx-auto rounded-lg shadow-lg border border-gray-200 hover:shadow-xl transition-shadow duration-300 cursor-pointer"
                style={{ minHeight: '500px', objectFit: 'contain' }}
              />
            </div>
            <div className="text-center">
              <h3 className="text-xl font-semibold text-gray-900 mb-6">Test Matrix Generation</h3>
              <img 
                src="/2.png"
                alt="TestMind Interface Screenshot 2" 
                className="w-full max-w-6xl mx-auto rounded-lg shadow-lg border border-gray-200 hover:shadow-xl transition-shadow duration-300 cursor-pointer"
                style={{ minHeight: '500px', objectFit: 'contain' }}
              />
            </div>
            <div className="text-center">
              <h3 className="text-xl font-semibold text-gray-900 mb-6">Results and Export</h3>
              <img 
                src="/3.png"
                alt="TestMind Interface Screenshot 3" 
                className="w-full max-w-6xl mx-auto rounded-lg shadow-lg border border-gray-200 hover:shadow-xl transition-shadow duration-300 cursor-pointer"
                style={{ minHeight: '500px', objectFit: 'contain' }}
              />
            </div>
          </div>
        </div>

        <div className="text-center">
          <div className="bg-gradient-to-r from-primary-50 to-blue-50 rounded-xl p-8 md:p-12 shadow-lg border border-primary-100">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-6">Ready to Get Started?</h2>
            <p className="text-gray-600 mb-8 text-lg max-w-2xl mx-auto leading-relaxed">
              Start generating comprehensive test matrices for your software applications today.
            </p>
            <a
              href="/"
              className="btn-primary inline-flex items-center gap-3 text-lg px-10 py-4 rounded-xl shadow-lg hover:shadow-xl transition-all duration-300"
            >
              Start Using TestMind
              <ArrowRight size={24} />
            </a>
          </div>
        </div>
      </div>
    </div>
  );
};

export default About; 