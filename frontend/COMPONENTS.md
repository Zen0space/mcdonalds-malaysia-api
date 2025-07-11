# Component Documentation
## McDonald's Malaysia Outlet Visualizer

### 📋 Overview
This document provides comprehensive documentation for all React components used in the McDonald's Malaysia Outlet Visualizer frontend application.

### 🏗️ Architecture
- **Framework**: Next.js 14 with App Router
- **Language**: TypeScript
- **Styling**: Tailwind CSS + Styled JSX
- **Mapping**: Native Leaflet (SSR-compatible)
- **State Management**: React Hooks (useState, useEffect)

---

## 🗺️ Core Components

### `Map.tsx`
**Main interactive map component displaying McDonald's outlets**

#### Features
- ✅ Interactive Leaflet map with custom markers
- ✅ 5KM radius circles around outlets
- ✅ Color-coded markers (Red: intersecting, Green: isolated)
- ✅ Rich popups with outlet information
- ✅ Intersection detection using Haversine formula
- ✅ SSR compatibility with dynamic imports

#### Props
```typescript
interface MapProps {
  outlets: Outlet[]                                    // Array of outlet data
  showRadius: boolean                                  // Show/hide radius circles
  intersectionData?: Map<number, OutletIntersectionData> // Intersection analysis
  onOutletClick?: (outlet: Outlet) => void            // Click handler
  selectedOutlet?: Outlet                             // Currently selected outlet
}
```

#### Key Methods
- `createCustomMarker(color, isHovered)` - Creates McDonald's-themed markers
- `getMarkerColor(outlet)` - Determines marker color based on intersections
- `createPopupContent(outlet)` - Generates rich HTML popup content

#### Performance Optimizations
- React.memo for preventing unnecessary re-renders
- Efficient marker and circle management
- Cleanup on component unmount

---

### `MapControls.tsx`
**Control panel for map filters and outlet information**

#### Features
- ✅ Expandable/collapsible interface
- ✅ Search functionality by name/address
- ✅ Feature filtering (24hrs, Drive-Thru, McCafe)
- ✅ Radius visibility toggle
- ✅ Outlet counter display
- ✅ Selected outlet information card

#### Props
```typescript
interface MapControlsProps {
  filters: FilterOptions                               // Current filter state
  onFiltersChange: (filters: FilterOptions) => void   // Filter change handler
  outletCount: number                                  // Total outlets
  filteredCount: number                                // Filtered outlets
  loadingIntersections?: boolean                       // Loading state
  intersectionData?: Map<number, OutletIntersectionData> // Intersection data
  selectedOutlet?: Outlet                             // Selected outlet
  onClearSelection?: () => void                       // Clear selection handler
}
```

#### Filter Options
```typescript
interface FilterOptions {
  showRadius: boolean
  features: {
    twentyFourHours: boolean
  }
  searchQuery: string
}
```

---

### `IntersectionLegend.tsx`
**Visual legend for intersection analysis**

#### Features
- ✅ Color-coded legend (Red: intersecting, Green: isolated)
- ✅ Real-time outlet counts
- ✅ Floating overlay positioning
- ✅ Responsive design (hidden on mobile)
- ✅ Glass morphism styling

#### Props
```typescript
interface IntersectionLegendProps {
  intersectionData: Map<number, OutletIntersectionData> // Intersection data
  isVisible: boolean                                    // Visibility toggle
}
```

#### Styling
- Fixed positioning (top-right corner)
- Backdrop blur effect
- Responsive breakpoints
- Accessibility-friendly colors

---

## 🔧 Utility Components

### `LoadingSpinner.tsx`
**Reusable loading indicator with McDonald's branding**

#### Features
- ✅ Three size variants (small, medium, large)
- ✅ Customizable loading message
- ✅ McDonald's red color scheme
- ✅ Smooth CSS animations

#### Props
```typescript
interface LoadingSpinnerProps {
  size?: 'small' | 'medium' | 'large'  // Size variant
  message?: string                      // Loading message
  className?: string                    // Additional CSS classes
}
```

#### Usage Examples
```tsx
<LoadingSpinner size="large" message="Loading outlets..." />
<LoadingSpinner size="small" className="my-custom-class" />
```

---

### `ErrorBoundary.tsx`
**Error handling component for graceful error recovery**

#### Features
- ✅ Catches JavaScript errors in component tree
- ✅ Displays user-friendly error messages
- ✅ Detailed error information for debugging
- ✅ Page reload functionality
- ✅ Comprehensive error logging

#### Props
```typescript
interface Props {
  children: ReactNode    // Child components to wrap
  fallback?: ReactNode   // Custom fallback UI
}
```

#### Error Handling
- Implements React's error boundary pattern
- Logs errors using custom logger utility
- Provides detailed error stack traces
- Offers recovery options to users

#### Usage
```tsx
<ErrorBoundary fallback={<CustomErrorUI />}>
  <MapComponent />
</ErrorBoundary>
```

---

## 📊 Data Types

### `Outlet`
```typescript
interface Outlet {
  id: number
  name: string
  address: string
  operating_hours?: string
  waze_link?: string
  latitude: number
  longitude: number
  created_at: string
  updated_at: string
}
```

### `OutletIntersectionData`
```typescript
interface OutletIntersectionData {
  hasIntersection: boolean
  intersectingOutlets: NeighborOutlet[]
}
```

### `NeighborOutlet`
```typescript
interface NeighborOutlet {
  id: number
  name: string
  distance_km: string
}
```

---

## 🎨 Styling Guidelines

### Color Palette
- **McDonald's Red**: `#dc2626` (Primary brand color)
- **Intersecting Outlets**: `#ef4444` (Red markers)
- **Isolated Outlets**: `#22c55e` (Green markers)
- **Radius Circles**: `#3b82f6` (Blue with 20% opacity)

### Typography
- **Font Family**: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto
- **Headings**: 600 weight, appropriate sizing
- **Body Text**: 400 weight, 14px base size

### Responsive Design
- **Mobile**: < 768px (simplified UI, hidden legend)
- **Tablet**: 768px - 1024px (medium layouts)
- **Desktop**: > 1024px (full feature set)

---

## 🚀 Performance Optimizations

### React.memo Usage
All components use `React.memo` to prevent unnecessary re-renders:
```tsx
const MyComponent = memo(function MyComponent(props) {
  // Component logic
})
```

### Efficient State Management
- Minimal state updates
- Proper dependency arrays in useEffect
- Debounced search functionality

### Memory Management
- Proper cleanup in useEffect
- Efficient marker and circle management
- Optimized intersection calculations

---

## 🧪 Testing Guidelines

### Component Testing
- Test all prop combinations
- Verify event handlers
- Check responsive behavior
- Validate accessibility

### Integration Testing
- Test component interactions
- Verify API integration
- Check error scenarios
- Performance testing

### Example Test Structure
```tsx
describe('MapComponent', () => {
  test('renders outlets correctly', () => {
    // Test implementation
  })
  
  test('handles filter changes', () => {
    // Test implementation
  })
})
```

---

## 📱 Accessibility Features

### ARIA Labels
- Proper labeling for interactive elements
- Screen reader support
- Keyboard navigation

### Color Contrast
- WCAG AA compliant color combinations
- High contrast mode support
- Color-blind friendly palette

### Keyboard Support
- Tab navigation
- Enter/Space key activation
- Escape key for closing modals

---

## 🔄 State Management

### Local State (useState)
- Component-specific state
- UI interaction state
- Form input state

### Effect Management (useEffect)
- API calls
- Event listeners
- Cleanup functions

### Props Drilling
- Minimal prop passing
- Efficient component composition
- Context API for shared state (if needed)

---

## 📦 Build & Deployment

### Development
```bash
npm run dev          # Start development server
npm run build        # Build for production
npm run start        # Start production server
```

### Production Optimizations
- Code splitting
- Tree shaking
- Image optimization
- Bundle analysis

---

## 🐛 Common Issues & Solutions

### SSR Compatibility
**Issue**: Leaflet not working with Next.js SSR
**Solution**: Dynamic imports with `ssr: false`

### Memory Leaks
**Issue**: Map instances not cleaned up
**Solution**: Proper useEffect cleanup

### Performance Issues
**Issue**: Too many re-renders
**Solution**: React.memo and proper dependency arrays

---

## 📚 Resources

### Documentation
- [Next.js Documentation](https://nextjs.org/docs)
- [Leaflet Documentation](https://leafletjs.com/reference.html)
- [React Documentation](https://react.dev/)

### Tools
- [TypeScript](https://www.typescriptlang.org/)
- [Tailwind CSS](https://tailwindcss.com/)
- [ESLint](https://eslint.org/)

---

**Last Updated**: January 2025  
**Version**: 1.0.0  
**Maintainer**: Development Team 