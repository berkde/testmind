import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Brain, MessageSquare, Info, Mail } from 'lucide-react';
import ConnectionStatus from './ConnectionStatus';

const Header = () => {
  const location = useLocation();

  const navItems = [
    { path: '/', label: 'Home', icon: Brain },
    { path: '/chat', label: 'Chat', icon: MessageSquare },
    { path: '/about', label: 'About', icon: Info },
    { path: '/contact', label: 'Contact', icon: Mail },
  ];

  return (
    <header className="bg-white border-b border-gray-200 shadow-sm">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          <div className="flex items-center">
            <Link to="/" className="flex items-center space-x-2">
              <img
                src="/banner.png"
                alt="TestMind Emblem"
                className="w-8 h-8 rounded-lg object-contain bg-white"
                style={{ border: '1.5px solid #6366f1', boxShadow: '0 1px 4px rgba(0,0,0,0.08)' }}
              />
              <span className="text-xl font-bold text-gray-900">TestMind</span>
            </Link>
          </div>

          <div className="flex items-center space-x-8">
            <ConnectionStatus />
            
            <nav className="flex space-x-8">
              {navItems.map((item) => {
                const Icon = item.icon;
                const isActive = location.pathname === item.path;
                
                return (
                  <Link
                    key={item.path}
                    to={item.path}
                    className={`flex items-center space-x-1 px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                      isActive
                        ? 'bg-primary-100 text-primary-700'
                        : 'text-gray-500 hover:text-gray-700 hover:bg-gray-100'
                    }`}
                  >
                    <Icon size={16} />
                    <span>{item.label}</span>
                  </Link>
                );
              })}
            </nav>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;
