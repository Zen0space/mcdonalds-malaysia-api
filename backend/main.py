"""
Main entry point for the McDonald's Malaysia API backend.
Serves the FastAPI application with outlet data.
"""

from src.api.app import app

# Export the app for uvicorn
__all__ = ["app"]

if __name__ == "__main__":
    import uvicorn
    
    print("🍟 Starting McDonald's Malaysia API...")
    print("📍 Serving outlet data for Kuala Lumpur")
    print("🌐 Access API docs at: http://localhost:8000/docs")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    ) 