# Frontend Development - Phase 4 Simplified
## McDonald's Malaysia Outlet Visualizer

### 📊 **Progress Status** (Updated: January 2025)
- 🎉 **Day 1: COMPLETED** - Project Setup & Foundation
- 🎉 **Day 2: COMPLETED** - Basic Map Implementation
- 🎉 **Day 3: COMPLETED** - 5KM Radius Implementation
- 🚧 **Day 4: READY TO START** - Intersection Detection & Highlighting
- ⏳ **Day 5: PENDING** - Polish, Testing & Deployment

### 🎯 **Core Requirements**
1. **Map Visualization**: Display all McDonald's outlets on an interactive map
2. **5KM Radius Catchment**: Show 5KM radius circles around each outlet
3. **Intersection Highlighting**: Mark outlets that intersect with other outlets' 5KM radius

### 🛠️ **Tech Stack**
- **Framework**: Next.js 14 (App Router) ✅
- **Map Library**: Native Leaflet (React Leaflet replaced for better SSR compatibility) ✅
- **Styling**: Tailwind CSS ✅
- **API Integration**: Axios ✅
- **State Management**: React useState/useEffect ✅

### 🎉 **Recent Accomplishments**
- ✅ **Fixed React Strict Mode Issues**: Replaced React Leaflet with native Leaflet implementation
- ✅ **API Integration Complete**: Full API service with error handling and TypeScript types
- ✅ **Environment Setup**: `.env.local` configured for localhost:8000
- ✅ **Connection Verified**: API test component confirms backend connectivity
- ✅ **Map Rendering**: Interactive map with proper cleanup and SSR compatibility

---

## 📅 **5-Day Development Plan**

### **Day 1: Project Setup & Foundation** ⏰ 4-6 hours
#### Task 1.1: Create Next.js Project
- [x] Initialize Next.js project with TypeScript ✅
- [x] Navigate to project directory and test initial setup ✅
- [x] Clean up default files and components ✅

#### Task 1.2: Install Dependencies
- [x] Install mapping dependencies (react-leaflet, leaflet, @types/leaflet) ✅
- [x] Install API and utility dependencies (axios) ✅
- [x] Verify all dependencies are installed correctly ✅

#### Task 1.3: Project Structure Setup
- [x] Create folder structure: ✅
  ```
  src/
  ├── app/
  │   ├── page.tsx (main map page) ✅
  │   └── layout.tsx ✅
  ├── components/
  │   ├── Map/
  │   │   ├── MapContainer.tsx ✅
  │   │   ├── OutletMarker.tsx (pending Day 2)
  │   │   └── RadiusCircle.tsx (pending Day 3)
  │   └── UI/
  │       ├── LoadingSpinner.tsx ✅
  │       └── ErrorMessage.tsx ✅
  ├── services/
  │   └── api.ts ✅
  ├── types/
  │   └── outlet.ts ✅
  └── utils/
      └── distance.ts (pending Day 3)
  ```

#### Task 1.4: API Integration Setup
- [x] Create API service (`services/api.ts`) ✅
- [x] Define outlet types (`types/outlet.ts`) ✅
- [x] Create environment variables for API URL ✅
- [x] Test API connection with a simple fetch ✅

**✅ Day 1 Success Criteria:** 🎉 **COMPLETED**
- ✅ Next.js project runs without errors
- ✅ All dependencies installed
- ✅ Project structure created
- ✅ API connection established

---

### **Day 2: Basic Map Implementation** ⏰ 6-8 hours

#### Task 2.1: Basic Map Component
- [x] Create `MapContainer.tsx` component ✅
- [x] Import and configure Leaflet CSS ✅
- [x] Set up basic map with center on Kuala Lumpur ✅
- [x] Configure map options (zoom, center, etc.) ✅
- [x] Handle dynamic imports for SSR compatibility ✅

#### Task 2.2: Fetch and Display Outlets 🔄 **NEXT UP**
- [x] Implement outlet data fetching from API✅
- [x] Create loading and error states✅
- [x] Handle API response and data transformation✅
- [x] Add error boundary for map component✅

#### Task 2.3: Outlet Markers
- [x] Create `OutletMarker.tsx` component✅
- [x] Display outlets as markers on map✅
- [x] Add custom marker icons for McDonald's✅
- [x] Implement popup with outlet information:✅
  - Outlet name✅
  - Address✅
  - Operating hours✅
  - Waze link✅

#### Task 2.4: Basic Styling
- [x] Add Tailwind CSS for layout✅
- [x] Style the map container (full viewport)✅
- [x] Style popup content✅
- [x] Add responsive design basics✅

**✅ Day 2 Success Criteria:**
- Interactive map displays correctly
- All outlets visible as markers
- Popups show outlet information
- No console errors
- Responsive on desktop and mobile

---

### **Day 3: 5KM Radius Implementation** ⏰ 6-8 hours ✅ **COMPLETED**

#### Task 3.1: Distance Calculation Utilities ✅ **COMPLETED**
- [x] Create `utils/distance.ts` with Haversine formula ✅
- [x] Implement function to calculate distance between two coordinates ✅
- [x] Add function to convert 5KM to map units (meters) ✅
- [x] Test distance calculations with known coordinates ✅

#### Task 3.2: Radius Circle Component ✅ **COMPLETED**
- [x] Create radius circles using Leaflet Circle (implemented in Map.tsx) ✅
- [x] Configure circle properties: ✅
  - 5KM radius (5000 meters) ✅
  - Semi-transparent fill (fillOpacity: 0.1) ✅
  - Distinct border color (blue #3b82f6) ✅
  - Proper styling and performance ✅
- [x] Add circle for each outlet ✅

#### Task 3.3: Circle Visualization ✅ **COMPLETED**
- [x] Display 5KM radius circles around each outlet ✅
- [x] Implement toggle to show/hide circles ✅
- [x] Add circle styling with appropriate colors ✅
- [x] Optimize performance for multiple circles ✅

#### Task 3.4: UI Controls ✅ **COMPLETED**
- [x] Add toggle button for radius visibility ✅
- [x] Create simple control panel (MapControls component) ✅
- [x] Add outlet counter display (filtered/total) ✅
- [x] Style control elements with modern design ✅

**✅ Day 3 Success Criteria:** 🎉 **ALL COMPLETED**
- ✅ 5KM radius circles display around all outlets
- ✅ Circles are properly sized and positioned
- ✅ Toggle functionality works
- ✅ Performance is acceptable with all circles visible
- ✅ UI controls are intuitive

---

### **Day 4: Intersection Detection & Highlighting** ⏰ 8-10 hours ✅ **COMPLETED**

#### Task 4.1: Intersection Detection Algorithm ✅ **COMPLETED**
- [x] Frontend-only intersection detection using distance calculations ✅
- [x] For each outlet, find outlets within 5KM radius ✅
- [x] Binary classification: intersecting vs isolated outlets ✅
- [x] Create data structure to store intersection data per outlet ✅

#### Task 4.2: Intersection Calculation ✅ **COMPLETED**
- [x] Calculate intersections using Haversine formula ✅
- [x] Store intersection data in component state ✅
- [x] Create map of outlet ID -> intersection data ✅
- [x] Add intersecting outlet names for popup display ✅

#### Task 4.3: Visual Highlighting ✅ **COMPLETED**
- [x] Create different marker styles for intersecting outlets ✅
- [x] Use binary color coding:
  - **Red**: Intersecting outlets (within 5KM of others) ✅
  - **Green**: Isolated outlets (no intersections) ✅
- [x] Remove fake density levels and use real intersection data ✅
- [x] Add visual legend ✅

#### Task 4.4: Enhanced Popups ✅ **COMPLETED**
- [x] Add intersection information to popups ✅
- [x] Show count of intersecting outlets within 5KM ✅
- [x] List names of intersecting outlets ✅
- [x] Add intersection indicator in popup ✅

**✅ Day 4 Success Criteria:** 🎉 **ALL COMPLETED**
- ✅ Intersection detection works correctly using frontend calculations
- ✅ Outlets are color-coded based on intersection status (Red/Green)
- ✅ Popups show intersection information
- ✅ Visual legend is clear and helpful
- ✅ Performance remains good with frontend calculations
- ✅ No fake data used - all based on real outlet positions

---

### **Day 5: Polish, Testing & Deployment** ⏰ 4-6 hours

#### Task 5.1: UI/UX Improvements
- [ ] Add loading spinner while fetching data
- [ ] Improve error handling with user-friendly messages
- [ ] Add smooth transitions and animations
- [ ] Optimize mobile responsiveness

#### Task 5.2: Feature Enhancements
- [ ] Add search functionality for outlets (using API search endpoint)
- [ ] Add feature filtering (24hrs, Drive-Thru, McCafe)
- [ ] Implement zoom to outlet feature
- [ ] Add statistics panel:
  - Total outlets
  - Outlets with neighbors
  - Average neighbor count per outlet
  - Market density insights
- [ ] Add export functionality (optional)

#### Task 5.3: Testing & Bug Fixes
- [ ] Test on different screen sizes
- [ ] Test with different browsers
- [ ] Verify all outlets load correctly
- [ ] Test neighbor detection API calls manually
- [ ] Fix any identified bugs

#### Task 5.4: Documentation & Deployment
- [ ] Create README.md with setup instructions
- [ ] Add comments to complex code sections
- [ ] Prepare for deployment (build optimization)
- [ ] Test production build locally

**✅ Day 5 Success Criteria:**
- Application is fully functional
- No critical bugs
- Good performance on all devices
- Ready for deployment
- Documentation is complete

---

## 🎯 **Technical Specifications**

### **Map Configuration**
```typescript
const MAP_CONFIG = {
  center: [3.139, 101.6869], // Kuala Lumpur center
  zoom: 11,
  minZoom: 10,
  maxZoom: 18,
  radius: 5000, // 5KM in meters
};
```

### **Color Scheme**
- **0 Neighbors**: Green (#22c55e) - Isolated outlets
- **1-2 Neighbors**: Orange (#f59e0b) - Moderate density
- **3+ Neighbors**: Red (#ef4444) - High density
- **Radius Circles**: Semi-transparent blue (#3b82f6, 20% opacity)

### **API Integration**
```typescript
// Confirmed API endpoints (backend already running on localhost:8000)
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
const ENDPOINTS = {
  outlets: '/api/v1/outlets',           // List/search outlets
  outletById: '/api/v1/outlets/{id}',   // Get specific outlet
  nearby: '/api/v1/outlets/nearby',     // Find nearby outlets
  stats: '/api/v1/stats'                // Database statistics
};
```

### **Performance Targets**
- **Initial Load**: < 3 seconds
- **Map Interaction**: < 100ms response time
- **Intersection Calculation**: < 1 second for all outlets
- **Memory Usage**: < 100MB for 50 outlets

---

## 🔧 **Development Commands**

```bash
# Install dependencies
npm install

# Development server
npm run dev

# Build for production
npm run build

# Start production server
npm start
```

---

## 📋 **Acceptance Criteria**

### **Must Have**
- [ ] Interactive map displaying all McDonald's outlets
- [ ] 5KM radius circles around each outlet
- [ ] Color-coded markers based on neighbor count
- [ ] Responsive design (mobile + desktop)
- [ ] Error handling for API failures
- [ ] Loading states for better UX

### **Should Have**
- [ ] Toggle for radius visibility
- [ ] Statistics panel
- [ ] Search functionality
- [ ] Outlet details in popups
- [ ] Performance optimization

### **Could Have**
- [ ] Export functionality
- [ ] Advanced filtering
- [ ] Zoom to outlet feature
- [ ] Intersection lines between outlets

---

## 🚀 **Getting Started**

1. **Prerequisites**
   - Node.js 18+ installed
   - Backend API running on localhost:8000
   - Basic knowledge of React/Next.js

2. **Quick Start**
   ```bash
   npx create-next-app@latest mcd-outlet-visualizer --typescript --tailwind --app
   cd mcd-outlet-visualizer
   npm install react-leaflet leaflet axios
   npm install -D @types/leaflet
   npm run dev
   ```

3. **Environment Setup**
   ```bash
   # .env.local
   NEXT_PUBLIC_API_URL=http://localhost:8000
   ```

---

## 🎯 **Success Metrics**
- All 50 outlets visible on map
- Neighbor detection 100% accurate
- Page load time < 3 seconds
- No JavaScript errors
- Mobile responsive
- Accessible on all modern browsers

---

**Total Estimated Time**: 28-38 hours (5-6 days)
**Complexity**: Beginner to Intermediate
**Priority**: High

*This simplified approach focuses on core functionality while maintaining professional quality and user experience.* 