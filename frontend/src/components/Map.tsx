'use client'

import { useEffect, useRef } from 'react'
import * as L from 'leaflet'
import { MAP_CONFIG } from '../utils/distance'

interface Outlet {
  id: number
  name: string
  address: string
  latitude: number
  longitude: number
  operating_hours?: string
  waze_link?: string
}

interface MapProps {
  outlets: Outlet[]
  showRadius: boolean
}

export default function Map({ outlets, showRadius }: MapProps) {
  const mapRef = useRef<L.Map | null>(null)
  const mapContainerRef = useRef<HTMLDivElement>(null)
  const circlesRef = useRef<L.Circle[]>([])

  // Create custom McDonald's marker icons
  const createCustomMarker = (color: string, isHovered: boolean = false) => {
    const size = isHovered ? 48 : 40
    const shadowSize = isHovered ? 6 : 4
    
    return L.divIcon({
      html: `
        <div class="mcd-marker" style="
          width: ${size}px;
          height: ${size}px;
          background: linear-gradient(135deg, ${color} 0%, ${color}dd 100%);
          border: 3px solid white;
          border-radius: 50%;
          box-shadow: 0 ${shadowSize}px ${shadowSize * 2}px rgba(0,0,0,0.3);
          display: flex;
          align-items: center;
          justify-content: center;
          font-weight: bold;
          font-size: ${size * 0.6}px;
          color: white;
          text-shadow: 0 1px 2px rgba(0,0,0,0.5);
          transition: all 0.2s ease;
          cursor: pointer;
        ">
          M
        </div>
      `,
      className: 'custom-mcd-marker',
      iconSize: [size, size],
      iconAnchor: [size / 2, size / 2],
      popupAnchor: [0, -size / 2 - 10]
    })
  }

  // Get marker color - using McDonald's red until density logic is implemented
  const getMarkerColor = (outlet: Outlet) => {
    return '#dc2626' // McDonald's red for all outlets
  }

  // Create custom popup content
  const createPopupContent = (outlet: Outlet) => {
    const color = getMarkerColor(outlet)
    return `
      <div class="mcd-popup">
        <div class="mcd-popup-header" style="
          background: linear-gradient(135deg, ${color} 0%, ${color}dd 100%);
          color: white;
          padding: 12px 16px;
          margin: -10px -10px 12px -10px;
          border-radius: 8px 8px 0 0;
          font-weight: bold;
          font-size: 16px;
          text-shadow: 0 1px 2px rgba(0,0,0,0.3);
        ">
          <div style="display: flex; align-items: center; gap: 8px;">
            <span style="
              background: white;
              color: ${color};
              width: 24px;
              height: 24px;
              border-radius: 50%;
              display: flex;
              align-items: center;
              justify-content: center;
              font-size: 14px;
              font-weight: bold;
            ">M</span>
            ${outlet.name}
          </div>
        </div>
        <div class="mcd-popup-content">
          <p style="margin: 0 0 8px 0; color: #666; font-size: 14px; line-height: 1.4;">
            📍 ${outlet.address}
          </p>
          ${outlet.operating_hours ? `
            <p style="margin: 0 0 8px 0; color: #666; font-size: 14px;">
              🕒 ${outlet.operating_hours}
            </p>
          ` : ''}
          ${outlet.waze_link ? `
            <a href="${outlet.waze_link}" target="_blank" style="
              display: inline-block;
              background: #00d4ff;
              color: white;
              padding: 6px 12px;
              border-radius: 4px;
              text-decoration: none;
              font-size: 12px;
              font-weight: bold;
              margin-top: 8px;
            ">
              🗺️ Open in Waze
            </a>
          ` : ''}
        </div>
      </div>
    `
  }

  useEffect(() => {
    if (!mapContainerRef.current) return

    // Initialize map with better styling
    const map = L.map(mapContainerRef.current, {
      zoomControl: false // We'll add custom zoom controls
    }).setView(MAP_CONFIG.center, MAP_CONFIG.zoom)

    // Add custom zoom control
    L.control.zoom({
      position: 'bottomright'
    }).addTo(map)

    // Add tile layer with better styling
    L.tileLayer('https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png', {
      attribution: '© OpenStreetMap contributors, © CARTO',
      subdomains: 'abcd',
      maxZoom: 19
    }).addTo(map)

    mapRef.current = map

    // Cleanup function
    return () => {
      if (mapRef.current) {
        mapRef.current.remove()
        mapRef.current = null
      }
    }
  }, [])

  // Add markers when outlets change
  useEffect(() => {
    if (!mapRef.current || !outlets.length) return

    // Clear existing markers and circles
    mapRef.current.eachLayer((layer) => {
      if (layer instanceof L.Marker || layer instanceof L.Circle) {
        mapRef.current!.removeLayer(layer)
      }
    })
    
    // Clear circles reference
    circlesRef.current = []

    // Add new markers
    outlets.forEach((outlet) => {
      if (outlet.latitude && outlet.longitude) {
        const color = getMarkerColor(outlet)
        const marker = L.marker([outlet.latitude, outlet.longitude], {
          icon: createCustomMarker(color)
        })

        // Add hover effects
        marker.on('mouseover', function(this: L.Marker) {
          this.setIcon(createCustomMarker(color, true))
        })

        marker.on('mouseout', function(this: L.Marker) {
          this.setIcon(createCustomMarker(color, false))
        })

        // Add popup
        marker.bindPopup(createPopupContent(outlet), {
          maxWidth: 300,
          className: 'custom-mcd-popup'
        })

        marker.addTo(mapRef.current!)
        
        // Add 5KM radius circle if enabled
        if (showRadius) {
          const circle = L.circle([outlet.latitude, outlet.longitude], {
            radius: MAP_CONFIG.radius, // 5KM in meters
            color: '#3b82f6',
            fillColor: '#3b82f6',
            fillOpacity: 0.1,
            weight: 2,
            opacity: 0.6
          }).addTo(mapRef.current!)
          
          circlesRef.current.push(circle)
        }
      }
    })

    // Fit map to show all outlets
    if (outlets.length > 0) {
      const group = L.featureGroup(
        outlets
          .filter(outlet => outlet.latitude && outlet.longitude)
          .map(outlet => L.marker([outlet.latitude, outlet.longitude]))
      )
      mapRef.current.fitBounds(group.getBounds().pad(0.1))
    }

    console.log(`Added ${outlets.length} outlets to map with custom styling`)
  }, [outlets, showRadius])

  return (
    <div className="map-wrapper">
      <div ref={mapContainerRef} className="map-container" />
    </div>
  )
} 