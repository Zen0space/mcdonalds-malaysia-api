'use client';

import React from 'react';
import { ChatMessage } from '@/types/chat';
import LocationCard from './LocationCard';
import { parseOutletInfo, isOutletMessage } from '@/utils/outletParser';

interface MessageBubbleProps {
  message: ChatMessage;
}

const MessageBubble: React.FC<MessageBubbleProps> = ({ message }) => {
  const isUser = message.role === 'user';
  
  // Check if this is an outlet information message
  const isOutlet = !isUser && isOutletMessage(message.content);
  const outlets = isOutlet ? parseOutletInfo(message.content) : null;
  
  if (isOutlet) {
    console.log('🏪 Outlet detected:', outlets);
  }

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
        max-w-[75%] rounded-2xl shadow-sm
        ${isUser 
          ? 'bg-blue-500 text-white rounded-br-sm px-4 py-3' 
          : isOutlet 
            ? 'bg-transparent p-0' 
            : 'bg-white text-gray-800 border border-gray-200 rounded-bl-sm px-4 py-3'
        }
      `}>
        {isOutlet && outlets ? (
          // Render outlet cards
          <div className="space-y-0">
            {outlets.map((outlet, index) => (
              <LocationCard key={index} outlet={outlet} />
            ))}
            {/* Timestamp for outlet cards */}
            <div className="text-xs text-gray-500 mt-2 px-1">
              {new Date(message.timestamp).toLocaleTimeString([], { 
                hour: '2-digit', 
                minute: '2-digit' 
              })}
            </div>
          </div>
        ) : (
          // Render regular text message
          <>
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
          </>
        )}
      </div>
    </div>
  );
};

export default MessageBubble; 