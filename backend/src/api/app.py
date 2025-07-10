"""
Main FastAPI application for McDonald's Malaysia API.
Clean, organized application with proper database integration.
"""

import time
import logging
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.exceptions import RequestValidationError

from .routes import router

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI application
app = FastAPI(
    title="McDonald's Malaysia API",
    description="""
    🍟 **McDonald's Malaysia Outlet API**
    
    A comprehensive RESTful API providing McDonald's outlet locations, coordinates, and details for Kuala Lumpur.
    
    ## 🚀 Features
    
    * **🗺️ Location Data**: Complete outlet information with GPS coordinates
    * **🔍 Text Search**: Search outlets by name or address
    * **📍 Nearby Search**: Find outlets within 5km radius using GPS coordinates
    * **🏷️ Feature Filtering**: Filter by outlet features (24hrs, Drive-Thru, McCafe)
    * **📊 Statistics**: Database and coverage statistics
    * **⚡ Fast**: Optimized for quick responses with response time headers
    * **🆓 Free**: No authentication required
    
    ## 📍 Coverage
    
    Currently covers **Kuala Lumpur** with 50+ McDonald's outlets including:
    - Shopping malls (KLCC, Pavilion, Mid Valley)
    - 24-hour locations
    - Drive-Thru outlets
    - McCafe locations
    
    ## 📖 Usage Examples
    
    ### Basic Operations
    ```
    GET /api/v1/outlets                    # List all outlets
    GET /api/v1/outlets/345               # Get specific outlet
    GET /api/v1/stats                     # Database statistics
    ```
    
    ### Search & Filter
    ```
    GET /api/v1/outlets?search=KLCC       # Search by name/address
    GET /api/v1/outlets?features=24hrs    # Filter by features
    GET /api/v1/outlets?sort=name&limit=10 # Sort and paginate
    ```
    
    ### Location-Based Search
    ```
    GET /api/v1/outlets/nearby?latitude=3.1570&longitude=101.7123&radius=2
    # Find outlets within 2km of KLCC
    ```
    
    ## 📊 Data Quality
    
    * ✅ **Names & Addresses**: 100% coverage
    * ✅ **Operating Hours**: 90%+ coverage  
    * ✅ **GPS Coordinates**: 90%+ coverage (required for nearby search)
    * ✅ **Waze Links**: Available for navigation
    * ✅ **Features**: Drive-Thru, 24hrs, McCafe classifications
    
    ## 🔧 Response Headers
    
    All responses include:
    - `X-Process-Time`: Request processing time in seconds
    - Standard CORS headers for browser compatibility
    
    ## 📝 Notes
    
    - All coordinates are validated within Malaysia bounds
    - Distance calculations use the Haversine formula
    - Nearby search limited to 5km radius for performance
    - All timestamps in ISO 8601 format
    """,
    version="1.0.0",
    contact={
        "name": "McDonald's Malaysia Scraper Project",
        "url": "https://github.com/user/geolocation-mcdscraper",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add request logging and timing middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log requests and add response time headers."""
    start_time = time.time()
    
    # Log request
    logger.info(f"📡 {request.method} {request.url.path} - Client: {request.client.host if request.client else 'unknown'}")
    
    # Process request
    response = await call_next(request)
    
    # Calculate response time
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(round(process_time, 4))
    
    # Log response
    logger.info(f"✅ {request.method} {request.url.path} - Status: {response.status_code} - Time: {process_time:.4f}s")
    
    return response

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Public API - allow all origins
    allow_credentials=False,  # No authentication required
    allow_methods=["GET"],  # Only GET methods for read-only API
    allow_headers=["*"],
)

# Global exception handler to ensure CORS headers are included in error responses
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Handle all exceptions and ensure CORS headers are included."""
    logger.error(f"❌ Unhandled exception: {str(exc)}")
    
    # Create error response with CORS headers
    response = JSONResponse(
        status_code=500,
        content={"detail": "Internal server error. Please check if database is configured properly."}
    )
    
    # Add CORS headers manually
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET"
    response.headers["Access-Control-Allow-Headers"] = "*"
    
    return response

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions and ensure CORS headers are included."""
    response = JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )
    
    # Add CORS headers manually
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET"
    response.headers["Access-Control-Allow-Headers"] = "*"
    
    return response

# Include API routes
app.include_router(router)

# Root endpoint - redirect to docs
@app.get("/", include_in_schema=False)
async def root():
    """Redirect root to API documentation."""
    return RedirectResponse(url="/docs")

# Health check at root level (for deployment monitoring)
@app.get("/health", include_in_schema=False)
async def root_health():
    """Root level health check for deployment monitoring."""
    return {"status": "healthy", "api": "McDonald's Malaysia API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    ) 