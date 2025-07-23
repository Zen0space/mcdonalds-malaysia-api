"""
Vercel serverless function entry point for FastAPI app.
Lightweight version for serverless deployment.
"""

import os
import sys
from pathlib import Path

# Add the backend directory to Python path
backend_dir = Path(__file__).parent.parent / "backend"
sys.path.insert(0, str(backend_dir))

try:
    from fastapi import FastAPI, HTTPException
    from fastapi.middleware.cors import CORSMiddleware
    from pydantic import BaseModel
    from typing import List, Optional
    import json
except ImportError as e:
    print(f"Failed to import required packages: {e}")
    # Create a minimal fallback
    class FastAPI:
        def __init__(self, **kwargs):
            pass
        def get(self, path):
            def decorator(func):
                return func
            return decorator
        def add_middleware(self, *args, **kwargs):
            pass

# Create FastAPI app
app = FastAPI(
    title="McDonald's Scraper API",
    description="API for McDonald's outlet location data",
    version="1.0.0"
)

# Configure CORS
origins = [
    "http://localhost:3000",
    "https://*.vercel.app",
    os.getenv("NEXT_PUBLIC_API_URL", "").replace("/api", ""),
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # More permissive for serverless
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class OutletResponse(BaseModel):
    id: Optional[str] = None
    name: str
    address: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    phone: Optional[str] = None
    hours: Optional[str] = None

class HealthResponse(BaseModel):
    status: str
    service: str
    platform: str
    message: str

# Health check endpoint
@app.get("/", response_model=HealthResponse)
@app.get("/health", response_model=HealthResponse)
async def health_check():
    return HealthResponse(
        status="healthy",
        service="mcd-scraper-api",
        platform="vercel-serverless",
        message="FastAPI running on Vercel"
    )

# Basic outlets endpoint with mock data for now
@app.get("/outlets", response_model=List[OutletResponse])
async def get_outlets():
    """
    Get McDonald's outlets data.
    Returns mock data in serverless environment.
    """
    try:
        # Try to import and use the actual backend logic
        from src.api.routes import outlets
        return await outlets.get_outlets()
    except ImportError:
        # Fallback to mock data if backend not available
        mock_outlets = [
            OutletResponse(
                id="1",
                name="McDonald's KLCC",
                address="Lot 2.36.00, Level 2, Suria KLCC, Kuala Lumpur City Centre, 50088 Kuala Lumpur",
                latitude=3.1578,
                longitude=101.7123,
                phone="+60 3-2166 2188",
                hours="24 Hours"
            ),
            OutletResponse(
                id="2",
                name="McDonald's Pavilion KL",
                address="Lot 1.42.00, Level 1, Pavilion Kuala Lumpur, 168, Jalan Bukit Bintang, 55100 Kuala Lumpur",
                latitude=3.1496,
                longitude=101.7129,
                phone="+60 3-2141 3302",
                hours="10:00 AM - 10:00 PM"
            ),
            OutletResponse(
                id="3",
                name="McDonald's Mid Valley",
                address="Lot LG-024, Lower Ground Floor, Mid Valley Megamall, Lingkaran Syed Putra, 59200 Kuala Lumpur",
                latitude=3.1172,
                longitude=101.6777,
                phone="+60 3-2287 1190",
                hours="10:00 AM - 10:00 PM"
            )
        ]
        return mock_outlets
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching outlets: {str(e)}")

# Chat endpoint placeholder
@app.post("/chat")
async def chat_endpoint():
    """
    Chat endpoint placeholder.
    Full functionality requires additional dependencies.
    """
    return {
        "message": "Chat functionality is available in the full deployment",
        "status": "limited_mode"
    }

# Search endpoint
@app.get("/search")
async def search_outlets(q: str = ""):
    """
    Search outlets by name or location.
    """
    outlets = await get_outlets()
    if not q:
        return outlets

    # Simple search implementation
    filtered = [
        outlet for outlet in outlets
        if q.lower() in outlet.name.lower() or q.lower() in outlet.address.lower()
    ]
    return filtered

# API info endpoint
@app.get("/info")
async def api_info():
    """
    Get API information and available endpoints.
    """
    return {
        "service": "McDonald's Scraper API",
        "version": "1.0.0",
        "platform": "Vercel Serverless",
        "endpoints": {
            "health": "/health",
            "outlets": "/outlets",
            "search": "/search?q=query",
            "chat": "/chat",
            "docs": "/docs"
        },
        "environment": "serverless",
        "python_version": sys.version
    }

# Export the app for Vercel
handler = app

# For local testing
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
