'use client';

import React from 'react';
import ChatToggleButton from './ChatToggleButton';
import ChatPanel from './ChatPanel';
import { useChatSession } from '@/hooks/useChatSession';

const FloatingChatbot: React.FC = () => {
  const chatSession = useChatSession();

  return (
    <div className="fixed bottom-0 right-0 z-[10000] pointer-events-none">
      <div className="pointer-events-auto">
        {chatSession.isOpen && (
          <div className="mb-4">
            <ChatPanel 
              chatSession={chatSession}
              onClose={chatSession.closeChat}
            />
          </div>
        )}
        <div className="flex justify-end pr-6 pb-6">
          <ChatToggleButton 
            isOpen={chatSession.isOpen}
            onClick={chatSession.toggleChat}
            hasUnreadMessages={false}
          />
        </div>
      </div>
    </div>
  );
};

export default FloatingChatbot; 