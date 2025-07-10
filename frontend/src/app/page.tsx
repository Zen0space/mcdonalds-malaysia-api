'use client'

import { useEffect, useState } from 'react'
import dynamic from 'next/dynamic'
import MapControls, { FilterOptions } from '../components/MapControls'
import IntersectionLegend from '../components/IntersectionLegend'
import { isWithinRadius, calculateDistance, MAP_CONFIG } from '../utils/distance'

interface Outlet {
  id: number
  name: string
  address: string
  latitude: number
  longitude: number
  operating_hours?: string
  waze_link?: string
  features?: Record<string, any> | null
}

interface NeighborOutlet extends Outlet {
  distance_km: number
}

interface OutletIntersectionData {
  outletId: number
  hasIntersection: boolean
  intersectingOutlets: NeighborOutlet[]
}

// Dynamically import the map component to avoid SSR issues
const MapComponent = dynamic(() => import('../components/Map'), {
  ssr: false,
  loading: () => <div className="loading">Loading map...</div>
})

export default function Home() {
  const [outlets, setOutlets] = useState<Outlet[]>([])
  const [intersectionData, setIntersectionData] = useState<Map<number, OutletIntersectionData>>(new Map())
  const [loading, setLoading] = useState(true)
  const [loadingIntersections, setLoadingIntersections] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [selectedOutlet, setSelectedOutlet] = useState<Outlet | null>(null)
  const [filters, setFilters] = useState<FilterOptions>({
    showRadius: false,
    features: {
      twentyFourHours: false
    },
    searchQuery: ''
  })

  useEffect(() => {
    loadOutletsAndNeighbors()
  }, [])

  // Frontend-only intersection detection using distance calculations
  const calculateIntersections = (outlets: Outlet[]): Map<number, OutletIntersectionData> => {
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
  }

  const loadOutletsAndNeighbors = async () => {
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
      console.log(`Calculating intersections for ${validOutlets.length} outlets using frontend-only approach...`)
      
      // Use setTimeout to allow UI to update before heavy calculation
      setTimeout(() => {
        const intersections = calculateIntersections(validOutlets)
        setIntersectionData(intersections)
        setLoadingIntersections(false)
        console.log(`✅ Successfully calculated intersection data for ${intersections.size} outlets`)
      }, 100)
      
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load outlets')
      setLoading(false)
      setLoadingIntersections(false)
    }
  }

  // Filter outlets based on current filters
  const filteredOutlets = outlets.filter((outlet) => {
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

  if (loading) {
    return <div className="loading">Loading outlets...</div>
  }

  if (error) {
    return <div className="error">Error: {error}</div>
  }

  return (
    <div className="app-container">
      <MapControls
        filters={filters}
        onFiltersChange={setFilters}
        outletCount={outlets.length}
        filteredCount={filteredOutlets.length}
        loadingIntersections={loadingIntersections}
        intersectionData={intersectionData}
        selectedOutlet={selectedOutlet}
        onClearSelection={() => setSelectedOutlet(null)}
      />
      <IntersectionLegend 
        intersectionData={intersectionData}
        isVisible={!loadingIntersections && intersectionData.size > 0}
      />
      <MapComponent 
        outlets={filteredOutlets} 
        showRadius={filters.showRadius}
        intersectionData={intersectionData}
        loadingIntersections={loadingIntersections}
        onOutletClick={setSelectedOutlet}
        selectedOutlet={selectedOutlet}
      />
    </div>
  )
} 