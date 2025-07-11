/**
 * Custom hook for managing chat session state and operations
 */

import { useState, useCallback, useRef, useEffect } from 'react';
import { ChatState, ChatMessage, UserLocation } from '../types/chat';
import chatApi from '../services/chatApi';

const initialState: ChatState = {
  isOpen: false,
  sessionId: null,
  messages: [],
  isTyping: false,
  isLoading: false,
  error: null,
  userLocation: null,
};

export const useChatSession = () => {
  const [state, setState] = useState<ChatState>(initialState);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  /**
   * Scroll to bottom of messages
   */
  const scrollToBottom = useCallback(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, []);

  /**
   * Update state helper
   */
  const updateState = useCallback((updates: Partial<ChatState>) => {
    setState(prev => ({ ...prev, ...updates }));
  }, []);

  /**
   * Generate unique message ID
   */
  const generateMessageId = useCallback(() => {
    return `msg_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }, []);

  /**
   * Add message to chat
   */
  const addMessage = useCallback((content: string, role: 'user' | 'assistant') => {
    const message: ChatMessage = {
      id: generateMessageId(),
      content,
      role,
      timestamp: new Date(),
    };

    setState(prev => ({
      ...prev,
      messages: [...prev.messages, message],
    }));

    // Scroll to bottom after adding message
    setTimeout(scrollToBottom, 100);
  }, [generateMessageId, scrollToBottom]);

  /**
   * Create new chat session
   */
  const createSession = useCallback(async () => {
    updateState({ isLoading: true, error: null });

    try {
      const response = await chatApi.createSession();
      
      if (response.success && response.data) {
        updateState({
          sessionId: response.data.session_id,
          isLoading: false,
        });

        // Add welcome message
        if (response.data.welcome_message) {
          addMessage(response.data.welcome_message, 'assistant');
        }

        return response.data.session_id;
      } else {
        updateState({
          error: response.error || { message: 'Failed to create session' },
          isLoading: false,
        });
        return null;
      }
    } catch (error) {
      updateState({
        error: { message: 'Failed to create session' },
        isLoading: false,
      });
      return null;
    }
  }, [updateState, addMessage]);

  /**
   * Send message to chatbot
   */
  const sendMessage = useCallback(async (message: string) => {
    const timestamp = new Date().toISOString();
    console.log(`📤 [${timestamp}] sendMessage: Starting to send message:`, message);
    console.log(`📤 [${timestamp}] sendMessage: Current location state:`, state.userLocation);
    console.log(`📤 [${timestamp}] sendMessage: Session ID:`, state.sessionId);
    
    if (!message.trim() || !state.sessionId) {
      console.log(`📤 [${timestamp}] sendMessage: Aborting - missing message or session ID`);
      return;
    }

    // Add user message immediately
    addMessage(message, 'user');
    updateState({ isTyping: true, error: null });

    try {
      const requestData = {
        message,
        session_id: state.sessionId,
        user_location: state.userLocation || undefined,
      };
      
      console.log(`📤 [${timestamp}] sendMessage: Sending request data:`, requestData);
      console.log(`📤 [${timestamp}] sendMessage: Location included:`, !!requestData.user_location);
      
      const response = await chatApi.sendMessage(requestData);

      if (response.success && response.data) {
        // Add bot response
        addMessage(response.data.response, 'assistant');
        updateState({ isTyping: false });
      } else {
        updateState({
          error: response.error || { message: 'Failed to send message' },
          isTyping: false,
        });
      }
    } catch (error) {
      updateState({
        error: { message: 'Failed to send message' },
        isTyping: false,
      });
    }
  }, [state.sessionId, state.userLocation, addMessage, updateState]);

  /**
   * Toggle chat open/closed
   */
  const toggleChat = useCallback(async () => {
    if (!state.isOpen) {
      // Opening chat
      updateState({ isOpen: true });
      
      // Create session if not exists
      if (!state.sessionId) {
        await createSession();
      }
    } else {
      // Closing chat
      updateState({ isOpen: false });
    }
  }, [state.isOpen, state.sessionId, createSession, updateState]);

  /**
   * Close chat
   */
  const closeChat = useCallback(() => {
    updateState({ isOpen: false });
  }, [updateState]);

  /**
   * Clear chat history
   */
  const clearChat = useCallback(() => {
    updateState({ messages: [] });
  }, [updateState]);

  /**
   * Set user location
   */
  const setUserLocation = useCallback((location: UserLocation | null) => {
    const timestamp = new Date().toISOString();
    console.log(`🎯 [${timestamp}] useChatSession: setUserLocation called with:`, location);
    console.log(`🎯 [${timestamp}] useChatSession: Previous location was:`, state.userLocation);
    
    updateState({ userLocation: location });
    
    console.log(`🎯 [${timestamp}] useChatSession: Location state updated`);
  }, [updateState, state.userLocation]);

  /**
   * End chat session
   */
  const endSession = useCallback(async () => {
    if (state.sessionId) {
      try {
        await chatApi.deleteSession(state.sessionId);
      } catch (error) {
        console.error('Failed to delete session:', error);
      }
    }
    
    setState(initialState);
  }, [state.sessionId]);

  // Auto-scroll when messages change
  useEffect(() => {
    if (state.messages.length > 0) {
      scrollToBottom();
    }
  }, [state.messages, scrollToBottom]);

  return {
    // State
    ...state,
    messagesEndRef,
    
    // Actions
    toggleChat,
    closeChat,
    sendMessage,
    clearChat,
    setUserLocation,
    endSession,
    createSession,
  };
}; 