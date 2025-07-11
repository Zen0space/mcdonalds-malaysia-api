import { memo } from 'react'
import type { OutletIntersectionData } from '../types'

interface IntersectionLegendProps {
  intersectionData: Map<number, OutletIntersectionData>
  isVisible: boolean
}

/**
 * Visual legend component that displays intersection analysis information.
 * Shows color-coded legend for intersecting vs isolated outlets with counts.
 * Positioned as a floating overlay on the map with responsive design.
 * Optimized with React.memo for performance.
 * 
 * @param {IntersectionLegendProps} props - Component props
 * @param {Map<number, OutletIntersectionData>} props.intersectionData - Map of outlet intersection data
 * @param {boolean} props.isVisible - Whether the legend should be visible
 * @returns {JSX.Element | null} Legend component or null if not visible
 * 
 * @example
 * ```tsx
 * <IntersectionLegend 
 *   intersectionData={intersectionMap} 
 *   isVisible={showLegend} 
 * />
 * ```
 */
const IntersectionLegend = memo(function IntersectionLegend({ intersectionData, isVisible }: IntersectionLegendProps) {
  if (!isVisible) return null

  // Count intersecting vs isolated outlets
  const intersectingCount = Array.from(intersectionData.values()).filter(data => data.hasIntersection).length
  const isolatedCount = Array.from(intersectionData.values()).filter(data => !data.hasIntersection).length

  return (
    <div className="intersection-legend">
      <h3>🎯 5KM Radius Intersections</h3>
      <div className="legend-items">
        <div className="legend-item">
          <div className="legend-color intersecting"></div>
          <span>Intersecting ({intersectingCount})</span>
        </div>
        <div className="legend-item">
          <div className="legend-color isolated"></div>
          <span>Isolated ({isolatedCount})</span>
        </div>
      </div>
      
      <style jsx>{`
        .intersection-legend {
          position: fixed;
          top: 20px;
          right: 20px;
          z-index: 1000;
          background: rgba(255, 255, 255, 0.95);
          backdrop-filter: blur(10px);
          border: 1px solid rgba(255, 255, 255, 0.3);
          border-radius: 12px;
          padding: 16px;
          box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
          font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
          min-width: 200px;
        }

        @media (max-width: 768px) {
          .intersection-legend {
            display: none;
          }
        }
        
        .intersection-legend h3 {
          margin: 0 0 12px 0;
          font-size: 14px;
          font-weight: 600;
          color: #333;
        }
        
        .legend-items {
          display: flex;
          flex-direction: column;
          gap: 8px;
        }
        
        .legend-item {
          display: flex;
          align-items: center;
          gap: 8px;
          font-size: 13px;
          color: #555;
        }
        
        .legend-color {
          width: 16px;
          height: 16px;
          border-radius: 50%;
          border: 2px solid white;
          box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
        }
        
        .legend-color.intersecting {
          background: #ef4444;
        }
        
        .legend-color.isolated {
          background: #22c55e;
        }
      `}</style>
    </div>
  )
})

export default IntersectionLegend 