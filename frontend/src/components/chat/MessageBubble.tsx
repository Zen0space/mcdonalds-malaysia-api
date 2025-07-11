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
    <div className={`flex items-start gap-4 mb-6 animate-fadeIn ${isUser ? 'flex-row-reverse' : 'flex-row'}`}>
      {/* Avatar */}
      <div className={`
        w-10 h-10 rounded-full flex items-center justify-center text-white text-sm font-bold flex-shrink-0 shadow-md transition-transform hover:scale-105
        ${isUser 
          ? 'bg-gradient-to-br from-blue-500 to-blue-600' 
          : 'bg-gradient-to-br from-red-500 to-red-600'
        }
      `}>
        {isUser ? 'U' : 'M'}
      </div>

      {/* Message Content */}
      <div className={`
        max-w-[80%] transition-all duration-300 ease-out
        ${isUser 
          ? 'rounded-3xl rounded-br-lg bg-gradient-to-br from-blue-500 to-blue-600 text-white shadow-lg hover:shadow-xl px-5 py-4' 
          : isOutlet 
            ? 'bg-transparent p-0' 
            : 'rounded-3xl rounded-bl-lg bg-white text-gray-800 shadow-lg hover:shadow-xl border border-gray-100 px-5 py-4 backdrop-blur-sm'
        }
      `}>
        {isOutlet && outlets ? (
          // Render outlet cards
          <div className="space-y-3">
            {outlets.map((outlet, index) => (
              <div key={index} className="animate-slideUp" style={{ animationDelay: `${index * 100}ms` }}>
                <LocationCard outlet={outlet} />
              </div>
            ))}
            {/* Timestamp for outlet cards */}
            <div className="text-xs text-gray-400 mt-3 px-2 font-medium">
              {new Date(message.timestamp).toLocaleTimeString([], { 
                hour: '2-digit', 
                minute: '2-digit' 
              })}
            </div>
          </div>
        ) : (
          // Render regular text message
          <>
            <div className="text-sm leading-relaxed whitespace-pre-wrap font-medium">
              {message.content}
            </div>
            
            {/* Timestamp */}
            <div className={`
              text-xs mt-3 font-medium transition-opacity duration-200
              ${isUser ? 'text-blue-100 opacity-80' : 'text-gray-400 opacity-70'}
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