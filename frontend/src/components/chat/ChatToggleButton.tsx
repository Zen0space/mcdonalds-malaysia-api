'use client';

import React from 'react';

interface ChatToggleButtonProps {
  isOpen: boolean;
  onClick: () => void;
  hasUnreadMessages: boolean;
}

const ChatToggleButton: React.FC<ChatToggleButtonProps> = ({
  isOpen,
  onClick,
  hasUnreadMessages,
}) => {
  return (
    <button
      onClick={onClick}
      className={`
        w-16 h-16 bg-mcd-red hover:bg-mcd-dark-red 
        text-white rounded-full shadow-lg hover:shadow-xl
        transition-all duration-300 ease-in-out
        flex items-center justify-center
        focus:outline-none focus:ring-4 focus:ring-mcd-red/30
        transform hover:scale-105 active:scale-95
        ${isOpen ? 'rotate-45' : 'hover:animate-bounce-gentle'}
        relative
      `}
      aria-label={isOpen ? 'Close chat' : 'Open chat'}
    >
      {/* Unread indicator */}
      {hasUnreadMessages && !isOpen && (
        <div className="absolute -top-1 -right-1 w-4 h-4 bg-mcd-yellow rounded-full border-2 border-white animate-pulse" />
      )}
      
      {/* Icon */}
      <span className="text-2xl font-bold transition-transform duration-300">
        {isOpen ? '×' : '💬'}
      </span>
    </button>
  );
};

export default ChatToggleButton; 