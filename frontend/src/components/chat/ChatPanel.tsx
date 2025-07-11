'use client';

import React from 'react';
import ChatHeader from './ChatHeader';
import ChatMessages from './ChatMessages';
import ChatInput from './ChatInput';

interface ChatPanelProps {
  chatSession: any;
  onClose: () => void;
}

const ChatPanel: React.FC<ChatPanelProps> = ({ chatSession, onClose }) => {
  // Track component lifecycle
  React.useEffect(() => {
    const timestamp = new Date().toISOString();
    console.log(`📋 [${timestamp}] ChatPanel: Component MOUNTED`);
    
    return () => {
      const timestamp = new Date().toISOString();
      console.log(`📋 [${timestamp}] ChatPanel: Component UNMOUNTING`);
    };
  }, []);

  // Track re-renders
  React.useEffect(() => {
    const timestamp = new Date().toISOString();
    console.log(`📋 [${timestamp}] ChatPanel: Component RE-RENDERED`);
    console.log(`📋 [${timestamp}] ChatPanel: ChatSession state:`, {
      isOpen: chatSession.isOpen,
      sessionId: !!chatSession.sessionId,
      messagesCount: chatSession.messages.length,
      userLocation: chatSession.userLocation
    });
  });

  return (
    <div className="w-96 h-[600px] bg-white rounded-2xl shadow-2xl border border-gray-200 flex flex-col animate-slide-up">
      <ChatHeader 
        onClose={onClose}
        onClear={chatSession.clearChat}
        chatSession={chatSession}
      />
      
      <ChatMessages 
        messages={chatSession.messages}
        isTyping={chatSession.isTyping}
        messagesEndRef={chatSession.messagesEndRef}
      />
      
      <ChatInput 
        onSendMessage={chatSession.sendMessage}
        onClear={chatSession.clearChat}
        isLoading={chatSession.isLoading}
        disabled={!!chatSession.error}
      />
    </div>
  );
};

export default ChatPanel; 