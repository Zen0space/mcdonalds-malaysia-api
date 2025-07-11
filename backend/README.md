# McDonald's Malaysia Backend API

A FastAPI-based backend service that provides McDonald's outlet data for Malaysia with intelligent chatbot capabilities powered by Google Gemini 2.5 Flash.

## 🚀 Features

- **RESTful API** for McDonald's outlet data
- **Intelligent Chatbot** with Gemini 2.5 Flash integration
- **Location-based Search** with GPS coordinates
- **Real-time Data** with web scraping capabilities
- **Database Management** with SQLite/Turso support
- **Geocoding Services** for address-to-coordinates conversion
- **Function Calling** for dynamic data retrieval

## 📋 Prerequisites

- **Python 3.8+** (Recommended: Python 3.11+)
- **pip** (Python package manager)
- **Virtual environment** (recommended)
- **Gemini API Key** (for chatbot functionality)

## 🛠️ Installation

### 1. Clone and Navigate
```bash
git clone <repository-url>
cd geolocation-mcdscraper/backend
```

### 2. Create Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Install Playwright Browsers (for scraping)
```bash
playwright install
```

### 5. Database Setup
```bash
# Run database migration (adds features column if needed)
python migrate_db.py
```

**Note**: Environment variables are configured in the project root directory. See the [main README](../README.md) for environment setup instructions.

## 🚀 Quick Start

### 1. Start the API Server
```bash
# Development mode (with auto-reload)
python main.py

# Or using uvicorn directly
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 2. Access the API
- **API Documentation**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## 📚 API Endpoints

### Core Endpoints

#### Health Check
```http
GET /health
```
Returns API health status and database connectivity.

#### Get Nearby Outlets
```http
GET /api/outlets/nearby?lat=3.1570&lng=101.7123&radius=2.0&limit=20
```
Find McDonald's outlets near given coordinates.

**Parameters:**
- `lat` (float): Latitude coordinate
- `lng` (float): Longitude coordinate  
- `radius` (float, optional): Search radius in km (default: 2.0)
- `limit` (int, optional): Maximum results (default: 20)

#### Search Outlets
```http
GET /api/outlets/search?q=KLCC&limit=10
```
Search outlets by name or address.

**Parameters:**
- `q` (string): Search query
- `limit` (int, optional): Maximum results (default: 10)

#### Get Outlet Details
```http
GET /api/outlets/{outlet_id}
```
Get detailed information for a specific outlet.

### Chatbot Endpoints

#### Create Chat Session
```http
POST /api/chat/sessions
```
Create a new chat session with the AI assistant.

#### Send Message
```http
POST /api/chat/sessions/{session_id}/messages
```
Send a message to the AI assistant.

**Request Body:**
```json
{
  "message": "Find McDonald's near me",
  "user_location": {
    "lat": 3.1570,
    "lng": 101.7123
  }
}
```

## 🗂️ Project Structure

```
backend/
├── main.py                 # Application entry point
├── requirements.txt        # Python dependencies
├── migrate_db.py          # Database migration script
├── outlets.db             # SQLite database (auto-created)
└── src/
    ├── api/               # FastAPI application
    │   ├── app.py         # Main FastAPI app
    │   ├── routes.py      # API routes
    │   ├── models.py      # Pydantic models
    │   └── dependencies.py # Dependency injection
    ├── chatbot/           # AI chatbot functionality
    │   ├── gemini_client.py      # Gemini API client
    │   ├── chat_service.py       # Chat service logic
    │   ├── api_functions.py      # Function calling tools
    │   └── sync_api_functions.py # Sync wrappers
    ├── database/          # Database operations
    │   ├── connection.py  # Database connection
    │   ├── operations.py  # CRUD operations
    │   ├── models.py      # Database models
    │   └── schema.py      # Database schema
    ├── scraper/           # Web scraping
    │   ├── mcdonald_scraper.py   # Main scraper
    │   └── base_scraper.py       # Base scraper class
    └── geocoding/         # Geocoding services
        ├── nominatim_service.py  # Free geocoding
        └── validators.py         # Coordinate validation
```

## 🤖 Chatbot Setup

### 1. Get Gemini API Key
1. Visit [Google AI Studio](https://aistudio.google.com/)
2. Create a new API key
3. Add it to the project root `.env` file as `GEMINI_API_KEY`

### 2. Test Chatbot
```bash
# Start the server
python main.py

# Test chat endpoint
curl -X POST "http://localhost:8000/api/chat/sessions" \
  -H "Content-Type: application/json"
```

## 🕷️ Web Scraping

### Manual Scraping
```bash
# Run the scraper directly
cd src/scraper
python mcdonald_scraper.py
```

### Scraping Configuration
- **Target**: McDonald's Malaysia official website
- **Method**: Playwright + BeautifulSoup
- **Data**: Outlet names, addresses, coordinates, operating hours
- **Frequency**: Manual or scheduled

## 🧪 Testing

### Run Tests
```bash
# Install test dependencies (already in requirements.txt)
pip install pytest pytest-asyncio

# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_api.py
```

### Manual API Testing
```bash
# Test health endpoint
curl http://localhost:8000/health

# Test nearby outlets
curl "http://localhost:8000/api/outlets/nearby?lat=3.1570&lng=101.7123"

# Test search
curl "http://localhost:8000/api/outlets/search?q=KLCC"
```

## 🕷️ Web Scraper Usage

### Using scraper_runner.py

The `scraper_runner.py` script is located in the project root and provides a production-ready interface for scraping McDonald's outlet data.

#### Basic Usage
```bash
# Navigate to project root (not backend directory)
cd geolocation-mcdscraper

# Activate virtual environment
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux

# Run the production scraper
python scraper_runner.py
```

#### What the Scraper Does
1. **Scrapes McDonald's Malaysia website** for Kuala Lumpur outlets
2. **Extracts comprehensive data**:
   - Outlet name and address
   - Operating hours
   - Waze navigation links
   - GPS coordinates from Waze URLs
3. **Saves to database** with duplicate detection
4. **Provides detailed statistics** and progress reporting

#### Expected Output
```
🚀 McDonald's Malaysia Production Scraper v1.0
⚡ Production Ready - Efficient Data Extraction
================================================================================
🎯 Target: Kuala Lumpur McDonald's outlets
⚡ Starting production scraping...

🎉 PRODUCTION SCRAPING COMPLETE!
📊 Results Summary:
   🏪 Unique outlets found: 52
   🔄 Duplicates skipped: 3
   💾 Successfully saved to database: 52
   ❌ Database errors: 0
   🔗 Waze links extracted: 52
   🗺️  Geocoding successful: 52
   ⏱️ Total runtime: 45.2 seconds
   ⚡ Processing efficiency: 1.2 outlets/second
   📍 Waze link success rate: 100.0%

✅ Session ID: scraper_20250115_143022
🚀 Production scraping completed successfully!
```

#### Scraper Features
- **Headless Operation**: Runs in background without browser UI
- **Duplicate Detection**: Automatically skips existing outlets
- **Error Recovery**: Robust error handling and retry logic
- **Progress Tracking**: Real-time statistics and session IDs
- **Database Integration**: Direct saving to SQLite/Turso database
- **Geocoding**: Automatic GPS coordinate extraction from Waze links

#### Configuration Options
The scraper can be configured by modifying `scraper_runner.py`:

```python
# Create scraper with custom settings
scraper = McDonaldMalaysiaScraper(
    headless=True,              # Run without browser UI
    debug=False,               # Production mode (clean logs)
    database_integration=True   # Save to database
)
```

#### Troubleshooting Scraper Issues
```bash
# If scraper fails to start
playwright install

# If database connection fails
python migrate_db.py

# If import errors occur
cd backend
pip install -r requirements.txt
```

## 📊 Database Management

### Database Connection (connection.py)

The `src/database/connection.py` module handles all database connectivity using Turso (LibSQL).

#### Connection Configuration
```python
from src.database.connection import DatabaseConnection, get_db_client

# Using context manager (recommended)
with DatabaseConnection() as client:
    result = client.execute("SELECT * FROM outlets LIMIT 5")
    print(result.rows)

# Using global client
client = get_db_client()
result = client.execute("SELECT COUNT(*) as count FROM outlets")
print(f"Total outlets: {result.rows[0]['count']}")
```

#### Connection Features
- **Automatic Connection Management**: Handles connection lifecycle
- **Context Manager Support**: Use with `with` statements
- **Error Handling**: Comprehensive error messages for missing config
- **Global Instance**: Shared connection across the application
- **Environment Loading**: Automatically loads from project root `.env` file

#### Connection Troubleshooting
```bash
# Test database connection
python -c "
from src.database.connection import get_db_client
client = get_db_client()
result = client.execute('SELECT 1 as test')
print('Connection successful:', result.rows)
"

# Check environment variables (from project root)
python -c "
import os
from dotenv import load_dotenv
load_dotenv()
print('DB URL:', os.getenv('TURSO_DATABASE_URL')[:20] + '...' if os.getenv('TURSO_DATABASE_URL') else 'Not set')
print('Auth Token:', 'Set' if os.getenv('TURSO_AUTH_TOKEN') else 'Not set')
"
```

### Database Schema Management (schema.py)

The `src/database/schema.py` module defines the database structure and provides migration utilities.

#### Running Schema Creation
```bash
# Method 1: Using migrate_db.py (recommended)
python migrate_db.py

# Method 2: Manual schema execution
python -c "
from src.database.schema import get_schema_queries
from src.database.connection import get_db_client

client = get_db_client()
for query in get_schema_queries():
    client.execute(query)
    print('Executed:', query[:50] + '...')
print('Schema creation complete!')
"
```

#### Database Schema Structure
```sql
-- Main outlets table
CREATE TABLE outlets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,          -- McDonald's outlet name
    address TEXT NOT NULL,              -- Full address
    operating_hours TEXT,               -- Operating hours (if available)
    waze_link TEXT,                     -- Waze navigation URL
    latitude REAL,                      -- GPS latitude
    longitude REAL,                     -- GPS longitude
    features TEXT,                      -- JSON string of features
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Performance indexes
CREATE INDEX idx_outlets_name ON outlets(name);
CREATE INDEX idx_outlets_address ON outlets(address);
CREATE INDEX idx_outlets_location ON outlets(latitude, longitude);
CREATE INDEX idx_outlets_created_at ON outlets(created_at);

-- Auto-update trigger
CREATE TRIGGER update_outlets_updated_at
AFTER UPDATE ON outlets
FOR EACH ROW
BEGIN
    UPDATE outlets SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;
```

#### Schema Migration
```python
from src.database.schema import get_migration_queries
from src.database.connection import get_db_client

# Run migrations for existing databases
client = get_db_client()
for query in get_migration_queries():
    try:
        client.execute(query)
        print(f"Migration successful: {query[:30]}...")
    except Exception as e:
        print(f"Migration skipped (likely already applied): {e}")
```

#### Schema Features
- **Unique Constraints**: Prevents duplicate outlet entries
- **Automatic Timestamps**: Tracks creation and update times
- **Performance Indexes**: Optimized for location and search queries
- **Update Triggers**: Automatically maintains updated_at timestamps
- **Migration Support**: Safe updates for existing databases

### Database Operations

#### View Database Stats
```bash
# Connect to SQLite database
sqlite3 outlets.db

# Check table structure
.schema outlets

# Count outlets
SELECT COUNT(*) FROM outlets;

# View sample data
SELECT * FROM outlets LIMIT 5;

# Check for outlets with coordinates
SELECT COUNT(*) FROM outlets WHERE latitude IS NOT NULL;

# Find outlets by area (example: KLCC area)
SELECT name, address FROM outlets 
WHERE latitude BETWEEN 3.15 AND 3.16 
AND longitude BETWEEN 101.70 AND 101.72;
```

#### Backup Database
```bash
# Backup SQLite database
cp outlets.db outlets_backup_$(date +%Y%m%d).db

# Or export as SQL
sqlite3 outlets.db .dump > outlets_backup_$(date +%Y%m%d).sql

# Restore from backup
sqlite3 outlets.db < outlets_backup_20250115.sql
```

#### Database Maintenance
```python
# Clean up old data (example)
from src.database.connection import get_db_client

client = get_db_client()

# Remove test entries
client.execute("DELETE FROM outlets WHERE name LIKE '%test%'")

# Update missing coordinates (if needed)
client.execute("""
UPDATE outlets 
SET latitude = NULL, longitude = NULL 
WHERE latitude = 0 OR longitude = 0
""")

# Vacuum database (optimize storage)
client.execute("VACUUM")
```

## 🚨 Troubleshooting

### Common Issues

#### 1. Import Errors
```bash
# Ensure you're in the backend directory
cd backend

# Activate virtual environment
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux

# Reinstall dependencies
pip install -r requirements.txt
```

#### 2. Database Errors
```bash
# Run migration script
python migrate_db.py

# Check database file permissions
ls -la outlets.db
```

#### 3. Environment Variable Errors
```bash
# Check if .env exists in project root
ls -la ../.env

# Verify environment variables are loaded
python -c "
import os
from dotenv import load_dotenv
load_dotenv()
print('Gemini API Key:', 'Set' if os.getenv('GEMINI_API_KEY') else 'Not set')
"
```

#### 4. Playwright Issues
```bash
# Reinstall browsers
playwright install

# Install system dependencies (Linux)
playwright install-deps
```

### Logs and Debugging

- **API Logs**: Check console output when running `python main.py`
- **Scraper Logs**: Located in `logs/` directory
- **Database Logs**: Enable with `DEBUG=true` in project root `.env`

## 🔄 Development Workflow

### 1. Development Setup
```bash
# Install development dependencies
pip install -r requirements.txt

# Enable debug mode (in project root .env)
echo "DEBUG=true" >> ../.env

# Start with auto-reload
python main.py
```

### 2. Code Formatting
```bash
# Install formatting tools
pip install black isort flake8

# Format code
black src/
isort src/

# Check code style
flake8 src/
```

### 3. Adding New Features

1. **API Endpoints**: Add routes in `src/api/routes.py`
2. **Database Models**: Update `src/database/models.py`
3. **Chatbot Functions**: Add to `src/chatbot/api_functions.py`
4. **Scraping Logic**: Extend `src/scraper/mcdonald_scraper.py`

## 📈 Performance Optimization

### Database Optimization
- **Indexes**: Automatically created for location queries
- **Connection Pooling**: Handled by libsql-client
- **Query Optimization**: Use appropriate limits and filters

### API Optimization
- **Caching**: Consider Redis for frequently accessed data
- **Rate Limiting**: Implement for production deployment
- **Async Operations**: Already implemented with FastAPI

## 🚀 Production Deployment

### Docker Deployment
```dockerfile
# Dockerfile example
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN playwright install

COPY . .
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Environment Variables for Production
See the [main README](../README.md) for complete environment configuration.

## 📞 Support

### Getting Help
1. **Documentation**: Check API docs at `/docs` endpoint
2. **Main README**: See [project root README](../README.md) for environment setup
3. **Issues**: Create GitHub issues for bugs
4. **Logs**: Check console output and log files
5. **Database**: Use SQLite browser for data inspection

### Contributing
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

**Happy coding! 🍟🚀** 