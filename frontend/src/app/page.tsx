'use client'

import { useEffect, useState, useCallback, useMemo } from 'react'
import dynamic from 'next/dynamic'
import MapControls from '../components/MapControls'
import IntersectionLegend from '../components/IntersectionLegend'
import ErrorBoundary from '../components/ErrorBoundary'
import LoadingSpinner from '../components/LoadingSpinner'
import { isWithinRadius, calculateDistance, MAP_CONFIG } from '../utils/distance'
import { logger } from '../utils/logger'
import { FloatingChatbot } from '../components/chat'


import type {
  Outlet,
  NeighborOutlet,
  OutletIntersectionData,
  FilterOptions,
} from '../types'

// Dynamically import the map component to avoid SSR issues
const MapComponent = dynamic(() => import('../components/Map'), {
  ssr: false,
  loading: () => <div className="loading">Loading map...</div>
})

/**
 * Main home page component that renders the McDonald's outlet mapping application.
 * Features include interactive map with outlets, filtering capabilities, and intersection analysis.
 * 
 * @returns {JSX.Element} The main application interface
 */
export default function Home() {
  const [outlets, setOutlets] = useState<Outlet[]>([])
  const [intersectionData, setIntersectionData] = useState<Map<number, OutletIntersectionData>>(new Map())
  const [loading, setLoading] = useState(true)
  const [loadingIntersections, setLoadingIntersections] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [selectedOutlet, setSelectedOutlet] = useState<Outlet | undefined>(undefined)
  const [filters, setFilters] = useState<FilterOptions>({
    showRadius: false,
    features: {
      twentyFourHours: false
    },
    searchQuery: ''
  })

  // useEffect moved below function definition

  /**
   * Calculate intersection data for outlets within 5KM radius of each other.
   * Uses Haversine formula for accurate distance calculations.
   * Memoized for performance optimization.
   * 
   * @param {Outlet[]} outlets - Array of outlet data
   * @returns {Map<number, OutletIntersectionData>} Map of outlet IDs to intersection data
   */
  const calculateIntersections = useCallback((outlets: Outlet[]): Map<number, OutletIntersectionData> => {
    const intersectionMap = new Map<number, OutletIntersectionData>()
    
    outlets.forEach(outlet => {
      // Find all outlets that intersect with this outlet's 5KM radius
      const intersectingOutlets: NeighborOutlet[] = []
      
      outlets.forEach(otherOutlet => {
        // Skip self
        if (otherOutlet.id === outlet.id) return
        
        // Check if within 5KM radius (intersection)
        if (isWithinRadius(
          outlet.latitude, outlet.longitude,
          otherOutlet.latitude, otherOutlet.longitude,
          MAP_CONFIG.radius // 5000 meters
        )) {
          // Calculate exact distance
          const distanceMeters = calculateDistance(
            outlet.latitude, outlet.longitude,
            otherOutlet.latitude, otherOutlet.longitude
          )
          
          intersectingOutlets.push({
            ...otherOutlet,
            distance_km: Math.round(distanceMeters / 1000 * 100) / 100 // Round to 2 decimal places
          })
        }
      })
      
      // Sort intersecting outlets by distance (closest first)
      intersectingOutlets.sort((a, b) => a.distance_km - b.distance_km)
      
      intersectionMap.set(outlet.id, {
        outletId: outlet.id,
        hasIntersection: intersectingOutlets.length > 0,
        intersectingOutlets
      })
    })
    
    return intersectionMap
  }, [])

  /**
   * Load outlets from the backend API and calculate intersection data.
   * Handles error states and loading states appropriately.
   * 
   * @async
   * @function loadOutletsAndNeighbors
   * @returns {Promise<void>}
   */
  const loadOutletsAndNeighbors = useCallback(async () => {
    try {
      setLoading(true)
      
      // First, fetch all outlets using the original method
      const response = await fetch('http://localhost:8000/api/v1/outlets')
      if (!response.ok) {
        throw new Error('Failed to fetch outlets')
      }
      const data = await response.json()
      
      // Filter outlets with valid coordinates
      const validOutlets = data.outlets.filter(
        (outlet: Outlet) => outlet.latitude && outlet.longitude
      )
      
      setOutlets(validOutlets)
      setLoading(false)
      
      // Calculate intersection data using frontend-only approach
      setLoadingIntersections(true)
      logger.info(`Calculating intersections for ${validOutlets.length} outlets using frontend-only approach`)
      
      // Use setTimeout to allow UI to update before heavy calculation
      setTimeout(() => {
        const intersections = calculateIntersections(validOutlets)
        setIntersectionData(intersections)
        setLoadingIntersections(false)
        logger.info(`Successfully calculated intersection data for ${intersections.size} outlets`)
      }, 100)
      
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load outlets')
      setLoading(false)
      setLoadingIntersections(false)
    }
  }, [calculateIntersections])

  // Load outlets on component mount
  useEffect(() => {
    loadOutletsAndNeighbors()
  }, [loadOutletsAndNeighbors])

  /**
   * Filter outlets based on current filter criteria.
   * Supports search by name/address and 24-hour outlet filtering.
   * Memoized for performance optimization.
   * 
   * @returns {Outlet[]} Filtered array of outlets
   */
  const filteredOutlets = useMemo(() => {
    return outlets.filter((outlet) => {
      // Search filter
      if (filters.searchQuery) {
        const query = filters.searchQuery.toLowerCase()
        const matchesName = outlet.name.toLowerCase().includes(query)
        const matchesAddress = outlet.address.toLowerCase().includes(query)
        if (!matchesName && !matchesAddress) return false
      }

      // Feature filters using operating_hours field
      // Only filtering by 24-hour outlets since that's the only real data we have
      if (filters.features.twentyFourHours) {
        const hours = outlet.operating_hours?.toLowerCase() || ''
        
        // Check for 24-hour outlets using operating_hours field
        const is24Hours = hours.includes('24 hours') || hours.includes('24')
        if (!is24Hours) return false
      }

      return true
    })
  }, [outlets, filters])

  if (loading) {
    return (
      <div className="loading-container">
        <LoadingSpinner 
          size="large" 
          message="Loading McDonald's outlets..." 
        />
        <style jsx>{`
          .loading-container {
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            background: #f8f9fa;
          }
        `}</style>
      </div>
    )
  }

  if (error) {
    return (
      <div className="error-container">
        <div className="error-content">
          <h2>🚨 Failed to Load</h2>
          <p>Error: {error}</p>
          <button onClick={() => window.location.reload()}>
            Retry
          </button>
        </div>
        <style jsx>{`
          .error-container {
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            background: #f8f9fa;
          }
          .error-content {
            text-align: center;
            padding: 2rem;
            background: white;
            border-radius: 8px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
          }
          .error-content button {
            background: #dc2626;
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 4px;
            cursor: pointer;
            margin-top: 16px;
          }
        `}</style>
      </div>
    )
  }

  return (
    <ErrorBoundary>
      <div className="app-container">
        <MapControls
          filters={filters}
          onFiltersChange={setFilters}
          outletCount={outlets.length}
          filteredCount={filteredOutlets.length}
          loadingIntersections={loadingIntersections}
          intersectionData={intersectionData}
          selectedOutlet={selectedOutlet}
          onClearSelection={() => setSelectedOutlet(undefined)}
        />
        <IntersectionLegend 
          intersectionData={intersectionData}
          isVisible={!loadingIntersections && intersectionData.size > 0}
        />
        <MapComponent 
          outlets={filteredOutlets} 
          showRadius={filters.showRadius}
          intersectionData={intersectionData}
          onOutletClick={setSelectedOutlet}
          selectedOutlet={selectedOutlet}
        />
      </div>
      
      {/* Floating Chatbot - Outside app-container to avoid overflow:hidden clipping */}
      <FloatingChatbot />
      
      {/* System Diagnostics - Development Tool */}
      <div className="fixed top-4 right-4 z-50">
        
      </div>
      

    </ErrorBoundary>
  )
} 