'use client'

import { useEffect, useState } from 'react'
import dynamic from 'next/dynamic'
import MapControls, { FilterOptions } from '../components/MapControls'

// Dynamically import the map component to avoid SSR issues
const MapComponent = dynamic(() => import('../components/Map'), {
  ssr: false,
  loading: () => <div className="loading">Loading map...</div>
})

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

export default function Home() {
  const [outlets, setOutlets] = useState<Outlet[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [filters, setFilters] = useState<FilterOptions>({
    showRadius: false,
    features: {
      twentyFourHours: false
    },
    searchQuery: ''
  })

  useEffect(() => {
    fetchOutlets()
  }, [])

  const fetchOutlets = async () => {
    try {
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
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load outlets')
      setLoading(false)
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
      />
      <MapComponent outlets={filteredOutlets} showRadius={filters.showRadius} />
    </div>
  )
} 