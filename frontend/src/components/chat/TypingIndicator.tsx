'use client';

import React from 'react';

const TypingIndicator: React.FC = () => {
  return (
    <div className="flex items-start gap-3">
      {/* Avatar */}
      <div className="w-8 h-8 bg-mcd-red rounded-full flex items-center justify-center text-white text-sm font-bold flex-shrink-0">
        M
      </div>

      {/* Typing Animation */}
      <div className="bg-white border border-gray-200 rounded-2xl rounded-bl-sm px-4 py-3 shadow-sm">
        <div className="flex items-center gap-2">
          <span className="text-gray-500 text-sm">McDonald&apos;s is typing</span>
          <div className="flex gap-1">
            <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce-dots" style={{ animationDelay: '0ms' }}></div>
            <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce-dots" style={{ animationDelay: '150ms' }}></div>
            <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce-dots" style={{ animationDelay: '300ms' }}></div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default TypingIndicator; 