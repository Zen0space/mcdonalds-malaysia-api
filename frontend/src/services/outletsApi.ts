/**
 * API service for McDonald's Malaysia Outlets
 */

export interface Outlet {
  id?: string
  name: string
  address: string
  latitude?: number
  longitude?: number
  phone?: string
  hours?: string
}

export interface ApiResponse<T> {
  success: boolean
  data?: T
  error?: {
    message: string
    details: string
  }
}

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || '/api'

class OutletsApiService {
  private baseUrl: string

  constructor() {
    this.baseUrl = `${API_BASE_URL}`
  }

  /**
   * Get all McDonald's outlets
   */
  async getOutlets(): Promise<ApiResponse<Outlet[]>> {
    try {
      const response = await fetch(`${this.baseUrl}/outlets`, {
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
      console.error('Failed to fetch outlets:', error)
      return {
        success: false,
        error: {
          message: 'Failed to fetch outlets',
          details: error instanceof Error ? error.message : 'Unknown error',
        },
      }
    }
  }

  /**
   * Search outlets by query
   */
  async searchOutlets(query: string): Promise<ApiResponse<Outlet[]>> {
    try {
      const response = await fetch(`${this.baseUrl}/search?q=${encodeURIComponent(query)}`, {
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
      console.error('Failed to search outlets:', error)
      return {
        success: false,
        error: {
          message: 'Failed to search outlets',
          details: error instanceof Error ? error.message : 'Unknown error',
        },
      }
    }
  }

  /**
   * Get API health status
   */
  async healthCheck(): Promise<ApiResponse<any>> {
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
      console.error('API health check failed:', error)
      return {
        success: false,
        error: {
          message: 'API health check failed',
          details: error instanceof Error ? error.message : 'Unknown error',
        },
      }
    }
  }

  /**
   * Get API information
   */
  async getApiInfo(): Promise<ApiResponse<any>> {
    try {
      const response = await fetch(`${this.baseUrl}/info`, {
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
      console.error('Failed to get API info:', error)
      return {
        success: false,
        error: {
          message: 'Failed to get API info',
          details: error instanceof Error ? error.message : 'Unknown error',
        },
      }
    }
  }
}

export const outletsApi = new OutletsApiService()
export default outletsApi
