"""
Vercel serverless function entry point for FastAPI app.
This file is required for Vercel to deploy the FastAPI backend.
"""

import os
import sys
from pathlib import Path

# Add the backend directory to Python path
backend_dir = Path(__file__).parent.parent / "backend"
sys.path.insert(0, str(backend_dir))

# Set environment variables if not already set
if "TURSO_DATABASE_URL" not in os.environ:
    os.environ["TURSO_DATABASE_URL"] = os.getenv("TURSO_DATABASE_URL", "")
if "TURSO_AUTH_TOKEN" not in os.environ:
    os.environ["TURSO_AUTH_TOKEN"] = os.getenv("TURSO_AUTH_TOKEN", "")

try:
    # Import the FastAPI app
    from src.api.app import app

    # Add CORS middleware for Vercel deployment
    from fastapi.middleware.cors import CORSMiddleware

    # Configure CORS for production
    origins = [
        "http://localhost:3000",
        "https://*.vercel.app",
        os.getenv("NEXT_PUBLIC_API_URL", "").replace("/api", ""),
    ]

    # Add CORS middleware if not already added
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Add a health check endpoint specifically for Vercel
    @app.get("/api/health")
    async def health_check():
        return {
            "status": "healthy",
            "service": "mcd-scraper-api",
            "platform": "vercel",
            "python_version": sys.version
        }

except ImportError as e:
    # Fallback app if imports fail
    from fastapi import FastAPI

    app = FastAPI(title="McDonald's Scraper API - Import Error")

    @app.get("/")
    async def import_error():
        return {
            "error": "Failed to import main application",
            "details": str(e),
            "hint": "Check if all dependencies are installed"
        }

# Export the app for Vercel
# Vercel expects the handler to be named 'app'
handler = app
