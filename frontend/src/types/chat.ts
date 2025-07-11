/**
 * TypeScript interfaces for McDonald's Malaysia Chatbot
 */

export interface ChatMessage {
  id: string;
  content: string;
  role: 'user' | 'assistant';
  timestamp: Date;
  isTyping?: boolean;
}

export interface ChatSession {
  sessionId: string;
  createdAt: string;
  status: 'active' | 'ended';
  welcomeMessage?: string;
}

export interface ChatResponse {
  response: string;
  session_id: string;
  message_type: 'response' | 'help' | 'error';
  context_used?: string;
  outlets_found?: number;
  follow_up_suggestions?: string[];
}

export interface ChatError {
  message: string;
  code?: string;
  details?: string;
}

export interface UserLocation {
  lat: number;
  lng: number;
}

export interface ChatState {
  isOpen: boolean;
  sessionId: string | null;
  messages: ChatMessage[];
  isTyping: boolean;
  isLoading: boolean;
  error: ChatError | null;
  userLocation: UserLocation | null;
}

export interface ChatApiResponse<T = any> {
  success: boolean;
  data?: T;
  error?: ChatError;
}

export interface SendMessageRequest {
  message: string;
  session_id: string;
  user_location?: UserLocation;
}

export interface CreateSessionResponse {
  session_id: string;
  created_at: string;
  status: string;
  welcome_message: string;
} 