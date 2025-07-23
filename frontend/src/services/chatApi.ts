/**
 * API service for McDonald's Malaysia Chatbot
 */

import {
  ChatApiResponse,
  CreateSessionResponse,
  ChatResponse,
  SendMessageRequest,
} from '../types/chat'

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || '/api'

class ChatApiService {
  private baseUrl: string

  constructor() {
    this.baseUrl = `${API_BASE_URL}`
  }

  /**
   * Create a new chat session
   */
  async createSession(): Promise<ChatApiResponse<CreateSessionResponse>> {
    try {
      const response = await fetch(`${this.baseUrl}/session`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({}),
      })

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      const data = await response.json()
      return { success: true, data }
    } catch (error) {
      console.error('Failed to create chat session:', error)
      return {
        success: false,
        error: {
          message: 'Failed to create chat session',
          details: error instanceof Error ? error.message : 'Unknown error',
        },
      }
    }
  }

  /**
   * Send a message to the chatbot
   */
  async sendMessage(
    request: SendMessageRequest
  ): Promise<ChatApiResponse<ChatResponse>> {
    try {
      const response = await fetch(`${this.baseUrl}/message`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(request),
      })

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      const data = await response.json()
      return { success: true, data }
    } catch (error) {
      console.error('Failed to send message:', error)
      return {
        success: false,
        error: {
          message: 'Failed to send message',
          details: error instanceof Error ? error.message : 'Unknown error',
        },
      }
    }
  }

  /**
   * Get chat history for a session
   */
  async getHistory(sessionId: string): Promise<ChatApiResponse<any>> {
    try {
      const response = await fetch(`${this.baseUrl}/history/${sessionId}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      })

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      const data = await response.json()
      return { success: true, data }
    } catch (error) {
      console.error('Failed to get chat history:', error)
      return {
        success: false,
        error: {
          message: 'Failed to get chat history',
          details: error instanceof Error ? error.message : 'Unknown error',
        },
      }
    }
  }

  /**
   * Delete a chat session
   */
  async deleteSession(sessionId: string): Promise<ChatApiResponse<any>> {
    try {
      const response = await fetch(`${this.baseUrl}/session/${sessionId}`, {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
        },
      })

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      const data = await response.json()
      return { success: true, data }
    } catch (error) {
      console.error('Failed to delete session:', error)
      return {
        success: false,
        error: {
          message: 'Failed to delete session',
          details: error instanceof Error ? error.message : 'Unknown error',
        },
      }
    }
  }

  /**
   * Check chat service health
   */
  async healthCheck(): Promise<ChatApiResponse<any>> {
    try {
      const response = await fetch(`${this.baseUrl}/health`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      })

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      const data = await response.json()
      return { success: true, data }
    } catch (error) {
      console.error('Chat service health check failed:', error)
      return {
        success: false,
        error: {
          message: 'Chat service health check failed',
          details: error instanceof Error ? error.message : 'Unknown error',
        },
      }
    }
  }
}

export const chatApi = new ChatApiService()
export default chatApi
