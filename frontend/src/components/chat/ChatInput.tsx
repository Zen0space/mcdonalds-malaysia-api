'use client';

import React, { useState } from 'react';
import LocationButton from '../LocationButton';

interface ChatInputProps {
  // eslint-disable-next-line no-unused-vars
  onSendMessage: (messageText: string) => void;
  onClear?: () => void;
  isLoading: boolean;
  disabled?: boolean;
}

const ChatInput: React.FC<ChatInputProps> = ({ 
  onSendMessage, 
  onClear,
  isLoading, 
  disabled = false 
}) => {
  const [message, setMessage] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (message.trim() && !isLoading && !disabled) {
      onSendMessage(message.trim());
      setMessage('');
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      if (message.trim() && !isLoading && !disabled) {
        onSendMessage(message.trim());
        setMessage('');
      }
    }
  };

  return (
    <div className="border-t border-gray-200 bg-white p-4 rounded-b-2xl">
      {/* Input Form */}
      <form onSubmit={handleSubmit} className="flex gap-2 items-center">
        {/* Clear Chat Button */}
        {onClear && (
          <button
            type="button"
            onClick={onClear}
            disabled={isLoading || disabled}
            className="w-10 h-10 bg-gray-100 hover:bg-gray-200 text-gray-600 rounded-full flex items-center justify-center transition-colors duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
            title="Clear chat"
          >
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
            </svg>
          </button>
        )}
        
        <div className="sm:hidden">
          <LocationButton 
            variant="secondary" 
            size="small" 
            showStatus={false}
            className="h-10 px-3"
          />
        </div>
        <input
          type="text"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Ask me anything about McDonald's..."
          disabled={isLoading || disabled}
          className="flex-1 px-4 py-3 bg-gray-100 border border-gray-300 rounded-full text-sm focus:outline-none focus:ring-2 focus:ring-mcd-red focus:border-transparent disabled:opacity-50 disabled:cursor-not-allowed"
        />
        <button
          type="submit"
          disabled={!message.trim() || isLoading || disabled}
          className="w-10 h-10 bg-mcd-red hover:bg-mcd-dark-red text-white rounded-full flex items-center justify-center transition-colors duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {isLoading ? (
            <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
          ) : (
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
            </svg>
          )}
        </button>
      </form>
    </div>
  );
};

export default ChatInput; 