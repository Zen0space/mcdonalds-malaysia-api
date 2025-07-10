'use client'

import { useState, memo } from 'react'
import type { FilterOptions, OutletIntersectionData, Outlet } from '../types'

interface MapControlsProps {
  filters: FilterOptions
  onFiltersChange: (_: FilterOptions) => void
  outletCount: number
  filteredCount: number
  loadingIntersections?: boolean
  intersectionData?: Map<number, OutletIntersectionData>
  selectedOutlet?: Outlet
  onClearSelection?: () => void
}

/**
 * Control panel component for map filters and outlet information.
 * Provides search functionality, feature filtering, and outlet statistics.
 * Optimized with React.memo for performance.
 * 
 * @param {MapControlsProps} props - Component props
    * @param {FilterOptions} props.filters - Current filter state
 * @param {function} props.onFiltersChange - Callback for filter changes
 * @param {number} props.outletCount - Total number of outlets
 * @param {number} props.filteredCount - Number of outlets after filtering
 * @param {boolean} props.loadingIntersections - Loading state for intersection calculations
 * @param {Map<number, OutletIntersectionData>} props.intersectionData - Intersection analysis data
 * @param {Outlet} props.selectedOutlet - Currently selected outlet
 * @param {function} props.onClearSelection - Callback to clear outlet selection
 * @returns {JSX.Element} Map controls component
 */
const MapControls = memo(function MapControls({ 
  filters, 
  onFiltersChange, 
  outletCount, 
  filteredCount, 
  loadingIntersections, 
  selectedOutlet, 
  onClearSelection 
}: MapControlsProps) {
  const [isExpanded, setIsExpanded] = useState(false)

  /**
   * Handle filter changes and update parent component state.
   * 
   * @param {keyof FilterOptions} key - Filter property to update
   * @param {boolean | string} value - New filter value
   */
  const handleFilterChange = (key: keyof FilterOptions, value: boolean | string) => {
    onFiltersChange({
      ...filters,
      [key]: value
    })
  }

  const handleFeatureChange = (feature: keyof FilterOptions['features']) => {
    onFiltersChange({
      ...filters,
      features: {
        ...filters.features,
        [feature]: !filters.features[feature]
      }
    })
  }

  return (
    <div className="map-controls">
      {/* Main Controls */}
      <div className="controls-header">
        <div className="controls-title">
                      <h3>🍟 McDonald&apos;s Map</h3>
          <div className="outlet-counter">
            <span className="count-primary">{filteredCount}</span>
            <span className="count-secondary">/ {outletCount} outlets</span>
            {loadingIntersections && (
              <div className="loading-indicator">
                <span className="loading-text">🔄 Calculating intersections...</span>
              </div>
            )}
          </div>
        </div>
        
        <button 
          className="expand-button"
          onClick={() => setIsExpanded(!isExpanded)}
          aria-label={isExpanded ? 'Collapse controls' : 'Expand controls'}
        >
          {isExpanded ? '▼' : '▶'}
        </button>
      </div>

      {/* Selected Outlet Card */}
      {selectedOutlet && (
        <div className="selected-outlet-card">
          <div className="selected-outlet-header">
            <div className="selected-outlet-icon">🎯</div>
            <div className="selected-outlet-content">
              <div className="selected-outlet-label">Selected Outlet</div>
              <div className="selected-outlet-name">{selectedOutlet.name}</div>
              {selectedOutlet.address && (
                <div className="selected-outlet-address">{selectedOutlet.address}</div>
              )}
            </div>
          </div>
          {onClearSelection && (
            <button 
              onClick={onClearSelection}
              className="clear-selection-button"
              aria-label="Clear selection"
            >
              <span className="clear-icon">✕</span>
              <span className="clear-text">Clear</span>
            </button>
          )}
        </div>
      )}

      {/* Expandable Controls */}
      {isExpanded && (
        <div className="controls-content">
          {/* Search */}
          <div className="control-group">
            <label htmlFor="search">🔍 Search Outlets</label>
            <input
              id="search"
              type="text"
              placeholder="Search by name or address..."
              value={filters.searchQuery}
              onChange={(e) => handleFilterChange('searchQuery', e.target.value)}
              className="search-input"
            />
          </div>

          {/* Radius Toggle */}
          <div className="control-group">
            <label className="toggle-label">
              <input
                type="checkbox"
                checked={filters.showRadius}
                onChange={(e) => handleFilterChange('showRadius', e.target.checked)}
                className="toggle-checkbox"
              />
              <span className="toggle-text">📍 Show 5KM Radius</span>
            </label>
          </div>

          {/* Feature Filters */}
          <div className="control-group">
            <label className="group-label">🏪 Filter by Features</label>
            <div className="filter-checkboxes">
              <label className="checkbox-label">
                <input
                  type="checkbox"
                  checked={filters.features.twentyFourHours}
                  onChange={() => handleFeatureChange('twentyFourHours')}
                  className="filter-checkbox"
                />
                <span>🕐 24 Hours</span>
              </label>
            </div>
          </div>

          {/* Quick Actions */}
          <div className="control-group">
            <div className="quick-actions">
              <button 
                className="action-button"
                onClick={() => onFiltersChange({
                  showRadius: false,
                  features: { twentyFourHours: false },
                  searchQuery: ''
                })}
              >
                🔄 Reset All
              </button>
              
              <button 
                className="action-button"
                onClick={() => handleFilterChange('showRadius', !filters.showRadius)}
              >
                {filters.showRadius ? '🚫 Hide Radius' : '📍 Show Radius'}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
})

export default MapControls 