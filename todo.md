# McDonald's Malaysia Scraper Project - Todo Checklist

## 🎯 Project Overview
**Goal:** Complete McDonald's Malaysia outlet scraper with frontend, visualization, and chatbot

**Tech Stack:** Python 3.11, Turso Database, FastAPI, React/Next.js, Chatbot Integration

**Architecture:** Monorepo (Single Repository) - No Docker

---

## 📁 **Project Structure**
```
geolocation-mcdscraper/
├── backend/                    # Python FastAPI backend
│   ├── src/
│   │   ├── scraper/           # Phase 1: Web scraping
│   │   ├── database/          # Phase 1: Database operations  
│   │   ├── geocoding/         # Phase 2: Geocoding service
│   │   ├── api/              # Phase 3: API endpoints
│   │   └── chatbot/          # Phase 5: Chatbot logic
│   ├── tests/
│   ├── requirements.txt
│   └── main.py
├── frontend/                   # React/Next.js frontend
│   ├── src/
│   │   ├── components/       # UI components
│   │   ├── pages/           # Application pages
│   │   ├── services/        # API integration
│   │   ├── utils/           # Utility functions
│   │   └── chatbot/         # Phase 5: Chat interface
│   ├── public/
│   ├── package.json
│   └── next.config.js
├── shared/                     # Shared utilities and types
│   ├── types/               # TypeScript types
│   └── constants/           # Shared constants
├── scripts/                    # Development scripts
│   ├── dev.py              # Run both backend and frontend
│   └── setup.py            # Initial setup script
├── .env.example
├── .gitignore
├── README.md
└── todo.md
```

---

## 📋 Phase 1: Web Scraping & Database Foundation (Days 1-3) ✅ **COMPLETE**

### 🔧 Environment Setup
- [x] Create Python 3.11 virtual environment
  ```bash
  py -3.11 -m venv venv
  venv\Scripts\activate
  ```
- [x] ⚠️ **Important**: Always activate virtual environment before working:
  ```bash
  # Windows
  venv\Scripts\activate
  # You should see (venv) in your prompt
  ```
- [x] ✅ **Dependency Isolation**: Created environment checker and documentation
  - Created `scripts/activate_env.py` to verify environment setup
  - Created `ENVIRONMENT_SETUP.md` with best practices
  - All packages properly isolated in virtual environment
- [x] Create project structure (backend folder)
- [x] Install backend packages:
  - [x] `playwright` (for web scraping)
  - [x] `beautifulsoup4` (for HTML parsing)
  - [x] `requests` (for HTTP requests)
  - [x] `libsql-client` (for Turso database)
  - [x] `pandas` (for data manipulation)
  - [x] `python-dotenv` (for environment variables)
- [x] Create `backend/requirements.txt` file
- [x] Set up `.env` file for configuration:
  - [x] `TURSO_DATABASE_URL` - Database connection
  - [x] `TURSO_AUTH_TOKEN` - Database authentication
  - [x] `GEOCODING_PROVIDER=nominatim` - Free geocoding service
  - [x] `GEMINI_API_KEY` - Google Gemini API key
  - [x] `CHATBOT_PROVIDER=gemini` - Chatbot service

### 🗄️ Database Schema Design
- [x] Design database schema for outlets table:
  ```sql
  CREATE TABLE outlets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    address TEXT NOT NULL,
    operating_hours TEXT,
    waze_link TEXT,
    latitude REAL,
    longitude REAL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
  );
  ```
- [x] Create database connection module
- [x] Implement database initialization script
- [x] Add data validation functions

### 🕷️ Web Scraping Implementation
- [x] Research McDonald's Malaysia website structure
  - [x] Analyze `https://www.mcdonalds.com.my/locate-us`
  - [x] Identify filter mechanism for "Kuala Lumpur"
  - [x] Study pagination system
  - [x] Check for JavaScript rendering requirements
- [x] Implement web scraper:
  - [x] Create base scraper class
  - [x] Add user-agent rotation
  - [x] Implement delay mechanisms (respectful scraping)
  - [x] Handle Kuala Lumpur filtering
  - [x] Extract outlet data:
    - [x] Name
    - [x] Address
    - [x] Operating hours
    - [x] Waze link
- [x] Implement pagination handler:
  - [x] Detect pagination elements
  - [x] Navigate through all pages
  - [x] Collect data from each page
- [x] Add error handling and retry logic
- [x] Implement data validation and cleaning

### 💾 Data Storage
- [x] Create data models/schemas
- [x] Implement database insertion functions
- [x] Add duplicate detection and handling
- [x] Create data backup functionality
- [x] Test data integrity
- [x] **Database Connection Working**: 
  - Fixed URL format: Use `https://` instead of `libsql://` for Turso
  - New auth token integrated successfully
  - Connection tested and verified

### ✅ Phase 1 Testing
- [x] Test scraper with small dataset
- [x] Verify database storage
- [x] Check data quality and completeness
- [x] Performance testing
- [x] **Database Fully Working**: 
  - Connection successful with https:// URL format
  - Schema created with tables, indexes, and triggers
  - CRUD operations tested and working
  - Sample data inserted and retrieved successfully

### 🎉 **Phase 1 COMPLETE** ✅
- **✅ Full Web Scraper**: Optimized production scraper implemented with sequential Waze extraction
- **✅ 50 KL Outlets**: Successfully extracted all McDonald's outlets in Kuala Lumpur
- **✅ Database Integration**: Complete CRUD operations with Turso database
- **✅ Advanced Features**: Deduplication, error handling, monitoring, validation
- **✅ Production Ready**: Comprehensive logging, retry logic, unique constraints
- **✅ 100% Waze Link Success**: All outlets have complete Waze links with GPS coordinates

---

## 📍 Phase 2: Geocoding Enhancement (Days 4-5) ✅ **COMPLETE**

### 🌐 Geocoding Service Setup (FREE OPTIONS)
- [x] **Primary Method:** Direct Waze Link Coordinate Extraction (100% accurate)
- [x] **Fallback Method:** OpenStreetMap Nominatim (completely free)
- [x] Install geocoding libraries:
  - [x] `geopy` for Nominatim (no API key needed)
  - [x] Custom Waze URL parsing (no API needed)
- [x] No rate limiting needed (Waze coordinates are direct extraction)

### 🗺️ Geocoding Implementation
- [x] Create comprehensive geocoding module (`backend/src/geocoding/mcdonald_geocoding.py`)
- [x] **Advanced Implementation:** Waze link coordinate extraction + Nominatim fallback
- [x] Implement address standardization for Malaysian addresses
- [x] Add geocoding functions:
  - [x] Single outlet geocoding with dual methods
  - [x] Batch geocoding with progress tracking
  - [x] Comprehensive error handling
  - [x] Multiple fallback strategies
- [x] Handle Malaysian address formats:
  - [x] State abbreviations (KL, W.P., etc.)
  - [x] Common address cleaning (phone numbers, emails removed)
  - [x] Address variations and progressive simplification

### 📊 Database Updates
- [x] Database schema includes coordinate columns (latitude, longitude)
- [x] Coordinate update functions integrated in scraper
- [x] Geocoding status tracking via statistics
- [x] All outlets have coordinates (no missing coordinates)
- [x] Real-time processing during scraping (no batch needed)

### 🔍 Quality Assurance
- [x] Validate geocoded coordinates:
  - [x] Check coordinates are within Malaysia bounds (1-7 lat, 99-119 lng)
  - [x] Verify coordinates match KL locations
  - [x] Automatic validation during extraction
- [x] Geocoding statistics and reports:
  - [x] **100% success rate achieved** (50/50 outlets)
  - [x] **100% Waze link extraction success**
  - [x] Real-time statistics tracking
- [x] **Production tested:** All 50 KL outlets successfully geocoded

### 🎉 **Phase 2 Results - EXCEEDED EXPECTATIONS**
- **✅ 100% Success Rate**: All 50 outlets have precise GPS coordinates
- **✅ Direct GPS Extraction**: More accurate than address-based geocoding
- **✅ Zero API Dependencies**: No rate limits or API keys needed for primary method
- **✅ Comprehensive Fallbacks**: Multiple strategies for edge cases
- **✅ Production Ready**: Integrated with scraper and database

---

## 🚀 Phase 3: API Development (Days 6-8) ✅ **COMPLETE**

### ⚡ FastAPI Backend Development ✅
- [x] Install FastAPI dependencies:
  - [x] `fastapi`
  - [x] `uvicorn`
  - [x] `pydantic`
  - [x] `python-multipart`
  - [x] `cors` middleware
- [x] Create clean FastAPI application structure with dependency injection
- [x] Implement comprehensive data models with Pydantic validation
- [x] Create enhanced API endpoints:
  - [x] `GET /api/v1/` - 🍟 API info with metadata
  - [x] `GET /api/v1/outlets` - 🏪 List/search/filter outlets with advanced features
  - [x] `GET /api/v1/outlets/{id}` - 🏪 Get specific outlet with full details
  - [x] `GET /api/v1/outlets/nearby` - 📍 GPS-based proximity search with Haversine formula
  - [x] `GET /api/v1/health` - 💚 Health check with database connectivity
  - [x] `GET /api/v1/stats` - 📊 Comprehensive database statistics
- [x] Add advanced query parameters and filtering:
  - [x] Text search by name/address (`search` parameter)
  - [x] Feature filtering (24hrs, Drive-Thru, McCafe via `features` parameter)
  - [x] GPS-based radius search with distance calculation
  - [x] Sorting options (name, id via `sort` parameter)
  - [x] Comprehensive pagination support (limit, offset, has_more)
- [x] Implement robust error handling and validation with proper HTTP status codes
- [x] Add CORS middleware for public API access
- [x] Add request logging middleware with response time tracking
- [x] Professional API documentation with Swagger/OpenAPI

### 📝 Enhanced API Documentation ✅
- [x] Write comprehensive API documentation with emoji-enhanced descriptions
- [x] Add detailed example requests and responses for all endpoints
- [x] Document error codes and handling with example responses
- [x] Create rich usage examples with multiple scenarios
- [x] Add technical notes about coordinate validation and distance calculations

### 🧪 Comprehensive Testing ✅
- [x] Test all API endpoints with real database
- [x] Test database connections through dependency injection
- [x] Verify geocoding functionality integration
- [x] Integration testing with 50 real outlets
- [x] Performance testing with response time headers

---

## 🎨 Phase 4: Frontend Development & Visualization (Days 9-12)

### 🔧 Frontend Setup
- [ ] Set up Node.js environment
- [ ] Choose frontend framework:
  - [ ] **Option A:** Next.js (React with SSR)
  - [ ] **Option B:** Create React App
  - [ ] **Option C:** Vite + React
- [ ] Create frontend project structure
- [ ] Install frontend dependencies:
  - [ ] React/Next.js
  - [ ] TypeScript
  - [ ] Tailwind CSS or Material-UI
  - [ ] Axios for API calls
  - [ ] React Query for state management

### 🗺️ Map Visualization
- [ ] Choose mapping library:
  - [ ] **Option A:** React Leaflet (free, lightweight, recommended)
  - [ ] **Option B:** Mapbox GL JS with React (good balance)
  - [ ] **Option C:** @react-google-maps/api (React-friendly Google Maps)
- [ ] Install mapping dependencies:
  - [ ] `react-leaflet` + `leaflet` (for Option A)
  - [ ] `mapbox-gl` + `react-map-gl` (for Option B)
  - [ ] `@react-google-maps/api` (for Option C)
- [ ] Implement map component:
  - [ ] Display all McDonald's outlets
  - [ ] Custom markers for outlets
  - [ ] Popup with outlet information
  - [ ] Zoom and pan functionality
  - [ ] Responsive design

### 📊 Data Visualization
- [ ] Install charting library:
  - [ ] Chart.js or Recharts
  - [ ] D3.js for advanced visualizations
- [ ] Create visualization components:
  - [ ] Outlet distribution by area
  - [ ] Operating hours analysis
  - [ ] Geographic density heatmap
  - [ ] Statistics dashboard

### 🎯 Core Frontend Features
- [ ] Create main pages:
  - [ ] Home/Dashboard page
  - [ ] Outlet list page
  - [ ] Outlet detail page
  - [ ] Search results page
  - [ ] About page
- [ ] Implement search functionality:
  - [ ] Text search by name/address
  - [ ] Location-based search
  - [ ] Filter by operating hours
  - [ ] Sort by distance
- [ ] Add responsive design:
  - [ ] Mobile-first approach
  - [ ] Tablet optimization
  - [ ] Desktop layout
- [ ] Implement navigation:
  - [ ] Header with navigation menu
  - [ ] Footer with links
  - [ ] Breadcrumbs
  - [ ] Back to top button

### 🔌 API Integration
- [ ] Create API service layer
- [ ] Implement data fetching:
  - [ ] Fetch all outlets
  - [ ] Search outlets
  - [ ] Get outlet details
  - [ ] Handle loading states
  - [ ] Error handling
- [ ] Add caching with React Query
- [ ] Implement optimistic updates

### 🎨 UI/UX Design
- [ ] Design system setup:
  - [ ] Color palette
  - [ ] Typography
  - [ ] Component library
  - [ ] Icons and imagery
- [ ] Create reusable components:
  - [ ] Outlet card component
  - [ ] Search bar component
  - [ ] Filter components
  - [ ] Loading skeletons
  - [ ] Error boundaries

---

## 🤖 Phase 5: Chatbot Integration (Days 13-15)

### 🧠 Chatbot Backend Development (FREE)
- [ ] Set up Google Gemini 2.5 Flash (free tier):
  - [ ] Get Gemini API key from Google AI Studio
  - [ ] Configure environment variables
- [ ] Install chatbot dependencies:
  - [ ] `google-generativeai` for Gemini integration (FREE)
  - [ ] `langchain` for LLM orchestration (optional)
- [ ] Create chatbot module:
  - [ ] Intent recognition
  - [ ] Context management
  - [ ] Response generation
  - [ ] McDonald's specific knowledge base

### 🔌 Chatbot API Endpoints
- [ ] Create chatbot API endpoints:
  - [ ] `POST /chat/message` - Send message to chatbot
  - [ ] `GET /chat/history` - Get chat history
  - [ ] `DELETE /chat/session` - Clear chat session
- [ ] Implement conversation features:
  - [ ] Outlet recommendations
  - [ ] Location-based queries
  - [ ] Operating hours inquiries
  - [ ] Direction assistance
  - [ ] General McDonald's information

### 💬 Chat Interface Frontend
- [ ] Create chat components:
  - [ ] Chat window component
  - [ ] Message bubble component
  - [ ] Input field with send button
  - [ ] Typing indicator
  - [ ] Chat history display
- [ ] Implement chat features:
  - [ ] Real-time messaging
  - [ ] Message persistence
  - [ ] Auto-scroll to latest message
  - [ ] Emoji support
  - [ ] File/image sharing (optional)

### 🎯 Chatbot Intelligence
- [ ] Train chatbot with McDonald's data:
  - [ ] Outlet information
  - [ ] Menu items (if available)
  - [ ] Common customer queries
  - [ ] Location-specific responses
- [ ] Implement smart features:
  - [ ] Location-aware responses
  - [ ] Personalized recommendations
  - [ ] Multi-language support (English/Malay)
  - [ ] Fallback responses

### 🔗 Integration Testing
- [ ] Test chatbot with frontend
- [ ] Test API integration
- [ ] User experience testing
- [ ] Performance optimization

---

## 🚀 Deployment & Production (Days 16-18)

### 🌐 Backend Deployment (Render)
- [ ] Prepare backend for deployment:
  - [ ] Update requirements.txt
  - [ ] Create startup script
  - [ ] Environment variable configuration
- [ ] Deploy to Render:
  - [ ] Connect GitHub repository
  - [ ] Set environment variables:
    - [ ] `TURSO_DATABASE_URL`
    - [ ] `TURSO_AUTH_TOKEN`
    - [ ] Geocoding API keys
    - [ ] Chatbot API keys
  - [ ] Configure build and start commands
- [ ] Test deployed backend API

### 🎨 Frontend Deployment
- [ ] Prepare frontend for deployment:
  - [ ] Build optimization
  - [ ] Environment variables for API URLs
  - [ ] Static asset optimization
- [ ] Deploy frontend:
  - [ ] **Option A:** Render Static Site
  - [ ] **Option B:** Vercel (for Next.js)
  - [ ] **Option C:** Netlify
- [ ] Configure API endpoints for production
- [ ] Test deployed frontend

### 🔧 Development Scripts
- [ ] Create development scripts:
  - [ ] `scripts/dev.py` - Run backend and frontend together
  - [ ] `scripts/setup.py` - Initial project setup
  - [ ] `scripts/test.py` - Run all tests
  - [ ] `scripts/deploy.py` - Deployment helper

### 📊 Monitoring & Maintenance
- [ ] Set up monitoring:
  - [ ] API uptime monitoring
  - [ ] Error tracking
  - [ ] Performance metrics
- [ ] Create maintenance tasks:
  - [ ] Database backups
  - [ ] Data freshness checks
  - [ ] API health checks

---

## 🎁 Bonus Features (Optional)

### 🔄 Data Maintenance
- [ ] Implement scheduled data updates
- [ ] Create data freshness monitoring
- [ ] Add data validation alerts

### 🌟 Enhanced Features
- [ ] Add outlet images scraping
- [ ] Implement outlet ratings/reviews
- [ ] Add real-time operating hours validation
- [ ] Create outlet comparison features
- [ ] Add favorites/bookmarks functionality
- [ ] Implement user reviews system

### 📱 Mobile App (Optional)
- [ ] React Native mobile app
- [ ] Progressive Web App (PWA)
- [ ] Mobile-specific features

---

## 🛠️ Technical Considerations

### 🔒 Security
- [ ] Implement API key authentication
- [ ] Add rate limiting
- [ ] Validate all input data
- [ ] Secure environment variable handling
- [ ] CORS configuration

### 📈 Performance
- [ ] Database indexing optimization
- [ ] API response caching
- [ ] Efficient pagination
- [ ] Frontend code splitting
- [ ] Image optimization

### 🐛 Error Handling
- [ ] Comprehensive logging
- [ ] Graceful error responses
- [ ] Retry mechanisms
- [ ] User-friendly error messages
- [ ] Monitoring and alerting

---

## 🚀 Development Workflow

### 📝 Daily Development
1. **Backend Development:** `cd backend && py -3.11 -m uvicorn main:app --reload`
2. **Frontend Development:** `cd frontend && npm run dev`
3. **Full Stack Development:** `python scripts/dev.py`

### 🧪 Testing
- **Backend Tests:** `cd backend && python -m pytest`
- **Frontend Tests:** `cd frontend && npm test`
- **Integration Tests:** `python scripts/test.py`

---

## 📚 Resources & References

### Documentation
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Next.js Documentation](https://nextjs.org/docs)
- [React Documentation](https://react.dev/)
- [Render Deployment Guide](https://render.com/docs)
- [Turso Documentation](https://docs.turso.tech/)

### Tools & Libraries
- [Playwright](https://playwright.dev/python/) - Web scraping
- [Leaflet](https://leafletjs.com/) - Interactive maps
- [Chart.js](https://www.chartjs.org/) - Data visualization
- [Tailwind CSS](https://tailwindcss.com/) - Styling
- [OpenAI API](https://openai.com/api/) - Chatbot integration

---

## 🎯 Success Metrics
- [ ] Successfully scrape all KL McDonald's outlets
- [ ] Achieve >95% geocoding accuracy
- [ ] API response time <500ms
- [ ] Frontend loads in <3 seconds
- [ ] Mobile responsive design
- [ ] Functional chatbot with >80% query success rate
- [ ] 99% uptime on production
- [ ] Complete documentation

---

**Estimated Timeline:** 18 days
**Priority:** High
**Status:** Ready to start

**Phase Breakdown:**
- **Phase 1-2:** Backend Foundation (5 days)
- **Phase 3:** API Development (3 days)
- **Phase 4:** Frontend & Visualization (4 days)
- **Phase 5:** Chatbot Integration (3 days)
- **Deployment:** Production Setup (3 days)

---

*Last updated: [Current Date]* 