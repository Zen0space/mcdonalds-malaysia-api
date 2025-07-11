'use client'

import { useEffect, useRef, memo, useCallback } from 'react'
import * as L from 'leaflet'
import { MAP_CONFIG } from '../utils/distance'
import { logger } from '../utils/logger'
import type { Outlet, OutletIntersectionData, NeighborOutlet } from '../types'

interface MapProps {
  outlets: Outlet[]
  showRadius: boolean
  intersectionData?: Map<number, OutletIntersectionData>
  onOutletClick?: (_: Outlet) => void
  selectedOutlet?: Outlet
}

/**
 * Interactive map component displaying McDonald's outlets with custom markers and radius circles.
 * Features include outlet visualization, intersection highlighting, and user interaction handling.
 * Optimized with React.memo for performance.
 * 
 * @param {MapProps} props - Component props
 * @param {Outlet[]} props.outlets - Array of outlet data to display
 * @param {boolean} props.showRadius - Whether to show 5KM radius circles
    * @param {Map<number, OutletIntersectionData>} props.intersectionData - Intersection analysis data
   * @param {function} props.onOutletClick - Callback for outlet marker clicks
 * @param {Outlet} props.selectedOutlet - Currently selected outlet
 * @returns {JSX.Element} Interactive map component
 */
const Map = memo(function Map({ outlets, showRadius, intersectionData, onOutletClick, selectedOutlet }: MapProps) {
  const mapRef = useRef<L.Map | null>(null)
  const mapContainerRef = useRef<HTMLDivElement>(null)
  const circlesRef = useRef<L.Circle[]>([])
  const selectedCircleRef = useRef<L.Circle | null>(null)
  const selectedMarkersRef = useRef<L.Marker[]>([])

  /**
   * Create custom McDonald's-themed marker icons with dynamic styling.
   * 
   * @param {string} color - Marker color (hex or CSS color)
   * @param {boolean} isHovered - Whether marker is in hover state
   * @returns {L.DivIcon} Custom Leaflet marker icon
   */
  const createCustomMarker = useCallback((color: string, isHovered: boolean = false) => {
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
  }, [])

  /**
   * Determine marker color based on intersection analysis data.
   * 
   * @param {Outlet} outlet - Outlet data
   * @returns {string} Hex color code for the marker
   */
  const getMarkerColor = useCallback((outlet: Outlet) => {
    if (!intersectionData || !intersectionData.has(outlet.id)) {
      return '#dc2626' // McDonald's red fallback
    }
    
    const data = intersectionData.get(outlet.id)
    // Simple binary coloring: Red if has intersection, Green if isolated
    return data?.hasIntersection ? '#ef4444' : '#22c55e'  // Red for intersecting, Green for isolated
  }, [intersectionData])

  /**
   * Generate HTML content for outlet popup with intersection information.
   * 
   * @param {Outlet} outlet - Outlet data
   * @returns {string} HTML string for popup content
   */
  const createPopupContent = useCallback((outlet: Outlet) => {
    const color = getMarkerColor(outlet)
    const intersectionInfo = intersectionData?.get(outlet.id)
    
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
          ${intersectionInfo ? `
            <div style="margin: 8px 0; padding: 8px; background: #f8f9fa; border-radius: 4px; border-left: 3px solid ${color};">
              <p style="margin: 0 0 4px 0; color: #333; font-size: 13px; font-weight: bold;">
                🎯 5KM Radius Intersection
              </p>
              <p style="margin: 0 0 4px 0; color: #666; font-size: 12px;">
                ${intersectionInfo.hasIntersection 
                  ? `🔴 Intersects with ${intersectionInfo.intersectingOutlets.length} outlet${intersectionInfo.intersectingOutlets.length === 1 ? '' : 's'}`
                  : '🟢 No intersections (isolated location)'
                }
              </p>
              ${intersectionInfo.hasIntersection && intersectionInfo.intersectingOutlets.length > 0 ? `
                <p style="margin: 4px 0 0 0; color: #666; font-size: 11px;">
                  <strong>Intersecting outlets:</strong><br/>
                  ${intersectionInfo.intersectingOutlets.slice(0, 3).map((outlet: NeighborOutlet) => 
                    `• ${outlet.name} (${outlet.distance_km}km)`
                  ).join('<br/>')}
                  ${intersectionInfo.intersectingOutlets.length > 3 ? `<br/>• ... and ${intersectionInfo.intersectingOutlets.length - 3} more` : ''}
                </p>
              ` : ''}
            </div>
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
  }, [getMarkerColor, intersectionData])

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
        marker.on('mouseover', () => {
          marker.setIcon(createCustomMarker(color, true))
        })

        marker.on('mouseout', () => {
          marker.setIcon(createCustomMarker(color, false))
        })

        // Add click handler
        marker.on('click', () => {
          if (onOutletClick) {
            onOutletClick(outlet)
          }
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

    logger.debug(`Added ${outlets.length} outlets to map with custom styling`)
  }, [outlets, showRadius, getMarkerColor, createCustomMarker, onOutletClick, createPopupContent])

  // Handle selected outlet - show individual radius and highlight intersecting outlets
  useEffect(() => {
    if (!mapRef.current) return

    // Always clear previous selected outlet visualization first
    if (selectedCircleRef.current) {
      mapRef.current.removeLayer(selectedCircleRef.current)
      selectedCircleRef.current = null
    }
    
    selectedMarkersRef.current.forEach(marker => {
      if (mapRef.current) {
        mapRef.current.removeLayer(marker)
      }
    })
    selectedMarkersRef.current = []

    // If no outlet is selected or no intersection data, just clear and return
    if (!selectedOutlet || !intersectionData) return

    // Add radius circle for selected outlet
    const selectedCircle = L.circle([selectedOutlet.latitude, selectedOutlet.longitude], {
      radius: MAP_CONFIG.radius, // 5KM in meters
      color: '#3b82f6', // Blue color to match the new design
      fillColor: '#3b82f6',
      fillOpacity: 0.15,
      weight: 3,
      opacity: 0.8,
      dashArray: '10, 10' // Dashed line to distinguish from regular circles
    }).addTo(mapRef.current)
    
    selectedCircleRef.current = selectedCircle

    // Get intersecting outlets for the selected outlet
    const intersectionInfo = intersectionData.get(selectedOutlet.id)
    if (intersectionInfo && intersectionInfo.hasIntersection) {
      // Add highlighted markers for intersecting outlets
      intersectionInfo.intersectingOutlets.forEach((intersectingOutlet: NeighborOutlet) => {
        const highlightMarker = L.marker([intersectingOutlet.latitude, intersectingOutlet.longitude], {
          icon: L.divIcon({
            html: `
              <div style="
                width: 50px;
                height: 50px;
                background: radial-gradient(circle, #fbbf24 0%, #f59e0b 100%);
                border: 4px solid white;
                border-radius: 50%;
                box-shadow: 0 0 20px rgba(251, 191, 36, 0.6);
                display: flex;
                align-items: center;
                justify-content: center;
                font-weight: bold;
                font-size: 18px;
                color: white;
                text-shadow: 0 2px 4px rgba(0,0,0,0.7);
                animation: pulse 2s infinite;
              ">
                M
              </div>
              <style>
                @keyframes pulse {
                  0%, 100% { transform: scale(1); }
                  50% { transform: scale(1.1); }
                }
              </style>
            `,
            className: 'highlighted-marker',
            iconSize: [50, 50],
            iconAnchor: [25, 25]
          })
        }).addTo(mapRef.current!)
        
        selectedMarkersRef.current.push(highlightMarker)
      })
    }

    // Center map on selected outlet
    mapRef.current.setView([selectedOutlet.latitude, selectedOutlet.longitude], 12, {
      animate: true,
      duration: 1
    })

  }, [selectedOutlet, intersectionData])

  return (
    <div className="map-wrapper">
      <div ref={mapContainerRef} className="map-container" />
    </div>
  )
})

export default Map 