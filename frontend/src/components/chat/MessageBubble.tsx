'use client';

import React from 'react';
import { ChatMessage } from '@/types/chat';

interface MessageBubbleProps {
  message: ChatMessage;
}

const MessageBubble: React.FC<MessageBubbleProps> = ({ message }) => {
  const isUser = message.role === 'user';

  return (
    <div className={`flex items-start gap-3 ${isUser ? 'flex-row-reverse' : 'flex-row'}`}>
      {/* Avatar */}
      <div className={`
        w-8 h-8 rounded-full flex items-center justify-center text-white text-sm font-bold flex-shrink-0
        ${isUser ? 'bg-blue-500' : 'bg-mcd-red'}
      `}>
        {isUser ? 'U' : 'M'}
      </div>

      {/* Message Content */}
      <div className={`
        max-w-[75%] rounded-2xl px-4 py-3 shadow-sm
        ${isUser 
          ? 'bg-blue-500 text-white rounded-br-sm' 
          : 'bg-white text-gray-800 border border-gray-200 rounded-bl-sm'
        }
      `}>
        <p className="text-sm leading-relaxed whitespace-pre-wrap">
          {message.content}
        </p>
        
        {/* Timestamp */}
        <div className={`
          text-xs mt-2 opacity-70
          ${isUser ? 'text-blue-100' : 'text-gray-500'}
        `}>
          {new Date(message.timestamp).toLocaleTimeString([], { 
            hour: '2-digit', 
            minute: '2-digit' 
          })}
        </div>
      </div>
    </div>
  );
};

export default MessageBubble; 