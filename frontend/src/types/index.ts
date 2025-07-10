/**
 * Core outlet data structure from the API
 */
export interface Outlet {
  id: number
  name: string
  address: string
  latitude: number
  longitude: number
  operating_hours?: string
  waze_link?: string
  features?: Record<string, unknown> | null
  created_at?: string
  updated_at?: string
}

/**
 * Outlet with distance information for nearby calculations
 */
export interface NeighborOutlet extends Outlet {
  distance_km: number
}

/**
 * Intersection data for each outlet
 */
export interface OutletIntersectionData {
  outletId: number
  hasIntersection: boolean
  intersectingOutlets: NeighborOutlet[]
}

/**
 * Filter options for the map controls
 */
export interface FilterOptions {
  showRadius: boolean
  features: {
    twentyFourHours: boolean
  }
  searchQuery: string
}

/**
 * Map configuration constants
 */
export interface MapConfig {
  center: [number, number]
  zoom: number
  minZoom: number
  maxZoom: number
  radius: number
}

/**
 * API response structure for outlets
 */
export interface OutletsApiResponse {
  outlets: Outlet[]
  total: number
  page?: number
  limit?: number
}

/**
 * Error response structure
 */
export interface ApiError {
  message: string
  status: number
  timestamp?: string
} 