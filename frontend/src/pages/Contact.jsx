import React from 'react';
import { Mail, Github } from 'lucide-react';
import berkImg from '../assets/berk.png';
import loriImg from '../assets/lori.png';
import jiaweiImg from '../assets/jiawei.png';
import adamImg from '../assets/adam.png';

const teamMembers = [
  {
    name: 'Berk',
    role: 'Lead Engineer and Architect',
    image: berkImg,
    github: 'https://github.com/berkde',
  },
  {
    name: 'Lori',
    role: 'Team Lead',
    image: loriImg,
    github: 'https://github.com/lms651',
  },
  {
    name: 'Jiawei',
    role: 'Frontend Engineer',
    image: jiaweiImg,
    github: 'https://github.com/jxc1687',
  },
  {
    name: 'Adam',
    role: 'Estimator',
    image: adamImg,
    github: 'https://github.com/adamc95',
  },
];

const faqs = [
  {
    question: 'How does TestMind generate test matrices?',
    answer: 'TestMind uses advanced AI language models to analyze your software requirements and automatically generate comprehensive test matrices based on user transitions and personas.'
  },
  {
    question: 'Can I export the generated test cases?',
    answer: 'Yes! TestMind supports Excel export functionality, allowing you to download test matrices and conversation history for use in your testing tools.'
  },
  {
    question: 'What types of applications does TestMind support?',
    answer: 'TestMind works with any software application that has user workflows, state transitions, and multiple user roles or personas.'
  },
  {
    question: 'Is my data secure when using TestMind?',
    answer: 'Absolutely. We prioritize data security and privacy. All conversations and generated data are handled with enterprise-grade security measures.'
  }
];

const Contact = () => {
  return (
    <div className="relative bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50 overflow-hidden min-h-screen">
      <div className="max-w-5xl mx-auto px-4 py-8">
        {/* Meet the Team Section */}
        <div className="text-center mb-12">
          <div className="flex justify-center mb-4">
            <img
              src="/banner.png"
              alt="TestMind Emblem"
              className="w-24 h-24 rounded-lg shadow-lg object-contain bg-white/80"
              style={{ border: '2px solid #fff' }}
            />
          </div>
          <h1 className="text-4xl font-bold text-gray-900 mb-4">Meet the Team</h1>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            We are a group of students passionate about building smart tools for software testing. Connect with us on GitHub!
          </p>
        </div>
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-8 mb-16">
          {teamMembers.map((member, idx) => (
            <div key={idx} className="card flex flex-col items-center text-center p-6">
              <img
                src={member.image}
                alt={member.name}
                className="w-24 h-24 rounded-full mb-4 object-cover border-4 border-primary-100 shadow"
              />
              <h3 className="font-semibold text-gray-900 text-lg mb-1">{member.name}</h3>
              <p className="text-primary-600 font-medium mb-2">{member.role}</p>
              <a
                href={member.github}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center gap-2 text-gray-700 hover:text-primary-600 font-medium mt-2"
              >
                <Github size={18} />
                GitHub
              </a>
            </div>
          ))}
        </div>

        <div>
          <h3 className="text-2xl font-bold text-gray-900 mb-6">Frequently Asked Questions</h3>
          <div className="space-y-4">
            {faqs.map((faq, index) => (
              <div key={index} className="border border-gray-200 rounded-lg p-4">
                <h4 className="font-semibold text-gray-900 mb-2">{faq.question}</h4>
                <p className="text-gray-600 text-sm">{faq.answer}</p>
              </div>
            ))}
          </div>
        </div>

        <div className="mt-12 text-center">
          <p className="text-gray-500 text-sm flex items-center justify-center gap-2">
            <Mail size={16} className="inline-block" />
            For questions, reach out to any of us on GitHub.
          </p>
        </div>
      </div>
    </div>
  );
};

export default Contact;
