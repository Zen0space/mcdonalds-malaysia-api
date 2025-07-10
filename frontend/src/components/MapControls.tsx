'use client'

import { useState } from 'react'

export interface FilterOptions {
  showRadius: boolean
  features: {
    twentyFourHours: boolean
  }
  searchQuery: string
}

interface MapControlsProps {
  filters: FilterOptions
  onFiltersChange: (filters: FilterOptions) => void
  outletCount: number
  filteredCount: number
}

export default function MapControls({ 
  filters, 
  onFiltersChange, 
  outletCount, 
  filteredCount 
}: MapControlsProps) {
  const [isExpanded, setIsExpanded] = useState(false)

  const handleFilterChange = (key: keyof FilterOptions, value: any) => {
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
          <h3>🍟 McDonald's Map</h3>
          <div className="outlet-counter">
            <span className="count-primary">{filteredCount}</span>
            <span className="count-secondary">/ {outletCount} outlets</span>
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
} 