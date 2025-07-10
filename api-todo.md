# McDonald's Malaysia API Development - Phase 3 Todo

## 🎯 **Goal: Create FastAPI Backend for McDonald's Outlet Data**

**Target**: Simple, clean API to serve the 50 KL McDonald's outlets with coordinates
**Deployment**: Render (Phase 4)
**Timeline**: Manageable step-by-step approach

---

## 📋 **Phase 3: API Development Checklist**

### 🔧 **Step 1: FastAPI Setup (Day 1 - Morning)** ✅ **COMPLETED**
- [x] Install FastAPI dependencies
  - [x] Add `fastapi` to requirements.txt
  - [x] Add `uvicorn[standard]` for ASGI server
  - [x] Add `python-multipart` for form data
  - [x] Fixed `libsql-client==0.3.1` version issue
- [x] Create basic API structure
  - [x] Create `backend/src/api/__init__.py`
  - [x] Create `backend/src/api/simple_main.py` (FastAPI app)
  - [x] Create `backend/src/api/simple_models.py` (Pydantic models)
  - [x] Create `backend/src/api/simple_routes.py` (API endpoints)

### 📊 **Step 2: Data Models (Day 1 - Afternoon)** ✅ **COMPLETED**
- [x] Create Pydantic response models
  - [x] `OutletBasic` model (basic outlet info)
  - [x] `OutletFull` model (complete outlet data)
  - [x] `HealthResponse` model (health check)
  - [x] `APIResponse` model (generic responses)
- [x] Add data validation
  - [x] Field validation with Pydantic
  - [x] Optional field handling
  - [x] Type validation (int, float, str, datetime)

### 🛣️ **Step 3: Basic Endpoints (Day 2 - Morning)** ✅ **COMPLETED**
- [x] Health check endpoint
  - [x] `GET /health` - API status with database connection check
  - [x] `GET /` - API info and available endpoints
- [x] Outlet endpoints (basic)
  - [x] `GET /api/v1/outlets` - List outlets (with limit parameter)
  - [x] `GET /api/v1/outlets/{id}` - Get specific outlet by ID
  - [x] Database integration working (50 outlets available)

### 🔍 **Step 4: Search & Filter (Day 2 - Afternoon)**
- [ ] Search functionality
  - [ ] `GET /outlets/search?q={query}` - Search by name
  - [ ] `GET /outlets/nearby?lat={lat}&lng={lng}&radius={km}` - Nearby search
- [ ] Filter options
  - [ ] Filter by features (24hrs, Drive-Thru, etc.)
  - [ ] Sort options (name, distance)
  - [ ] Pagination support

### 🌐 **Step 5: CORS & Middleware (Day 3 - Morning)** ✅ **PARTIALLY COMPLETED**
- [x] Add CORS middleware for frontend (public API, all origins allowed)
- [x] Add error handling middleware (HTTPException handling)
- [ ] Add request logging middleware
- [ ] Add response time headers

### 📚 **Step 6: Documentation (Day 3 - Afternoon)**
- [ ] Configure Swagger/OpenAPI docs
- [ ] Add endpoint descriptions
- [ ] Add example requests/responses
- [ ] Add API usage examples

### 🧪 **Step 7: Testing (Day 3 - Evening)** ✅ **COMPLETED**
- [x] Test all endpoints manually (test scripts created and passed)
- [x] Verify database connection works (50 outlets confirmed)
- [x] Test error handling (404 for missing outlets)
- [x] Test Pydantic models (validation working)
- [x] Environment variable loading tested

---

## 🎉 **PROGRESS SUMMARY**

### ✅ **COMPLETED (Steps 1, 2, 3, 5*, 7)**
- **FastAPI Setup**: Dependencies installed, basic structure created
- **Data Models**: Pydantic models with validation
- **Basic Endpoints**: Health check, outlet list, outlet by ID
- **CORS & Error Handling**: Public API with proper error responses
- **Testing**: All components tested and working

### 🚧 **REMAINING WORK**
- **Step 4**: Search & Filter endpoints (optional)
- **Step 6**: Enhanced documentation (optional)
- **Additional**: Stats endpoint, nearby search, pagination

### 🚀 **READY TO LAUNCH**
Current API can be started with:
```bash
uvicorn backend.src.api.simple_routes:app --reload
```
Visit: http://localhost:8000/docs

---

## 📁 **Planned File Structure**

```
backend/src/api/
├── __init__.py
├── main.py              # FastAPI app setup
├── models.py            # Pydantic response models
├── routes/
│   ├── __init__.py
│   ├── outlets.py       # Outlet endpoints
│   ├── search.py        # Search endpoints
│   └── health.py        # Health check endpoints
├── middleware/
│   ├── __init__.py
│   ├── cors.py          # CORS configuration
│   └── logging.py       # Request logging
└── utils/
    ├── __init__.py
    ├── database.py      # Database connection helper
    └── validators.py    # Custom validation functions
```

---

## 🎯 **API Endpoints Plan**

### **Core Endpoints (Must Have)**
```
GET  /                          # API info
GET  /health                    # Health check
GET  /outlets                   # List all outlets
GET  /outlets/{id}              # Get outlet by ID
GET  /stats                     # Database statistics
```

### **Search Endpoints (Nice to Have)**
```
GET  /outlets/search            # Search outlets
GET  /outlets/nearby            # Find nearby outlets
```

### **Query Parameters**
```
/outlets?limit=10&offset=0      # Pagination
/outlets?sort=name              # Sorting
/search?q=KLCC                  # Text search
/nearby?lat=3.1481&lng=101.7109&radius=5  # Location search
```

---

## 📊 **Response Format Examples**

### **Single Outlet Response**
```json
{
  "id": 1,
  "name": "McDonald's Bukit Bintang",
  "address": "Lot 1.01, Level 1, Pavilion KL...",
  "operating_hours": "24 Hours",
  "waze_link": "https://www.waze.com/live-map/directions?navigate=yes&to=ll.3.146847%2C101.710931",
  "latitude": 3.146847,
  "longitude": 101.710931,
  "features": ["24hrs", "McCafe"],
  "created_at": "2025-01-10T12:00:00Z",
  "updated_at": "2025-01-10T12:00:00Z"
}
```

### **Outlet List Response**
```json
{
  "outlets": [...],
  "total": 50,
  "limit": 10,
  "offset": 0,
  "has_more": true
}
```

---

## ❓ **Questions for Clarification**

### **🔧 Technical Decisions**
1. **Authentication**: Do you want any API authentication, or keep it public?
2. **Rate Limiting**: Should we add rate limiting to prevent abuse?
3. **Caching**: Do you want response caching for better performance?
4. **API Versioning**: Should we use `/v1/` prefix for future-proofing?

### **🎯 Feature Priorities**
5. **Search Complexity**: How advanced should the search be? (simple text vs fuzzy matching)
6. **Nearby Search**: What's the maximum radius you want to allow? (1km, 5km, 10km?)
7. **Additional Data**: Any other outlet information you want to expose via API?

### **🚀 Deployment Considerations**
8. **Environment Variables**: What config should be environment-specific?
9. **Database Connection**: Should API have its own DB connection or reuse scraper's?
10. **Logging Level**: What level of API logging do you want for production?

---

## 🚀 **Getting Started**

**Ready to begin?** Let me know:
1. Any clarifications needed on the plan above
2. Which technical decisions you prefer
3. If you want to start with Step 1 (FastAPI setup)

**Estimated Timeline**: 3 days for full API (can be done faster if we skip optional features)

**Next Step**: Once you approve this plan, I'll start with Step 1: FastAPI Setup 