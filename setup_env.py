#!/usr/bin/env python3
"""
Setup script to create .env file for McDonald's Malaysia API
"""
import os
from pathlib import Path

def create_env_file():
    """Create .env file with default configuration"""
    
    env_content = """# Database Configuration (FREE)
# IMPORTANT: Use https:// URL format, NOT libsql:// for remote Turso databases
TURSO_DATABASE_URL=https://mcd-scraper-tartnenas.aws-ap-northeast-1.turso.io
TURSO_AUTH_TOKEN=your_turso_auth_token_here

# Geocoding Service (FREE OPTIONS)
# OpenStreetMap Nominatim (completely free, no API key needed)
GEOCODING_PROVIDER=nominatim

# Chatbot Configuration (FREE OPTIONS)
# Google Gemini 2.5 Flash (free tier)
GEMINI_API_KEY=your_gemini_api_key_here
CHATBOT_PROVIDER=gemini

# Development Configuration
DEBUG=true
LOG_LEVEL=info

# Frontend Configuration
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_MAP_PROVIDER=react-leaflet  # Uses OpenStreetMap (completely free)

# Optional: Free map tile providers
NEXT_PUBLIC_MAP_TILES=openstreetmap  # openstreetmap, cartodb, stamen
"""
    
    env_file = Path(".env")
    
    if env_file.exists():
        print("❌ .env file already exists!")
        response = input("Do you want to overwrite it? (y/N): ")
        if response.lower() != 'y':
            print("Setup cancelled.")
            return
    
    try:
        with open(env_file, 'w') as f:
            f.write(env_content)
        
        print("✅ .env file created successfully!")
        print()
        print("🔧 IMPORTANT: You need to set up your Turso database:")
        print("1. Go to https://turso.tech and create a free account")
        print("2. Create a new database")
        print("3. Get your database URL and auth token")
        print("4. Replace 'your_turso_auth_token_here' in .env with your actual token")
        print()
        print("🚀 After setting up the database, run:")
        print("   cd backend")
        print("   python -m venv venv")
        print("   venv\\Scripts\\activate  # On Windows")
        print("   pip install -r requirements.txt")
        print("   python main.py")
        
    except Exception as e:
        print(f"❌ Error creating .env file: {e}")

if __name__ == "__main__":
    print("🍟 McDonald's Malaysia API - Environment Setup")
    print("=" * 50)
    create_env_file() 