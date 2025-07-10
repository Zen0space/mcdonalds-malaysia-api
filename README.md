# McDonald's Malaysia Scraper Project

A comprehensive web scraping and data visualization project that extracts McDonald's Malaysia outlet information, adds geocoding, and provides a full-stack web application with chatbot integration.

## 🎯 Project Overview

This project scrapes McDonald's Malaysia outlet data from their official website, enriches it with geographical coordinates, and serves it through a modern web application with visualization and chatbot features.

### Features

- **🕷️ Web Scraping**: Automated scraping of McDonald's Malaysia outlet data (✅ Complete)
- **🗺️ Geocoding**: Address-to-coordinates conversion with 100% success rate (✅ Complete)
- **🚀 Enhanced FastAPI Backend**: Professional RESTful API with advanced search & filtering (✅ Complete)
- **📍 GPS-Based Search**: Find nearby outlets using Haversine distance calculation (✅ Complete)
- **🎨 React Frontend**: Modern web interface with interactive maps (🚧 Phase 4)
- **📊 Data Visualization**: Charts and analytics dashboard (🚧 Phase 4)
- **🤖 Chatbot Integration**: AI-powered outlet recommendations and queries (🚧 Phase 5)

## 🏗️ Architecture

**Monorepo Structure** (Single Repository, No Docker)

```
geolocation-mcdscraper/
├── backend/                    # Python FastAPI backend
│   ├── src/
│   │   ├── scraper/           # Web scraping modules
│   │   ├── database/          # Database operations
│   │   ├── geocoding/         # Geocoding services
│   │   ├── api/              # API endpoints
│   │   └── chatbot/          # Chatbot logic
│   ├── tests/
│   ├── requirements.txt
│   └── main.py
├── frontend/                   # React/Next.js frontend
│   ├── src/
│   │   ├── components/       # UI components
│   │   ├── pages/           # Application pages
│   │   ├── services/        # API integration
│   │   └── chatbot/         # Chat interface
│   ├── package.json
│   └── next.config.js
├── shared/                     # Shared utilities
├── scripts/                    # Development scripts
└── todo.md                    # Project checklist
```

## 🚀 Tech Stack

### Backend ✅
- **Python 3.11** - Programming language
- **FastAPI** - Web framework with dependency injection
- **Turso (LibSQL)** - Cloud SQLite database
- **Playwright** - JavaScript-capable web scraping
- **Nominatim + Waze** - Geocoding services (100% free)
- **Pydantic** - Data validation and serialization
- **Google Gemini** - Chatbot integration (planned)

### Frontend
- **React/Next.js** - Web framework
- **TypeScript** - Type safety
- **Tailwind CSS** - Styling
- **React Leaflet** - Interactive maps (React-friendly)
- **Chart.js** - Data visualization

### Deployment
- **Render** - Cloud hosting platform
- **GitHub** - Version control and CI/CD

## 🔧 Getting Started

### Prerequisites

- Python 3.11 installed
- Node.js (for frontend)
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/geolocation-mcdscraper.git
   cd geolocation-mcdscraper
   ```

2. **Set up Python 3.11 virtual environment**
   ```bash
   py -3.11 -m venv venv
   venv\Scripts\activate  # Windows
   # or
   source venv/bin/activate  # Linux/Mac
   ```

3. **Install backend dependencies**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp env.example .env
   # Edit .env with your actual API keys and database credentials
   ```

5. **Install Playwright browsers (for web scraping)**
   ```bash
   playwright install
   ```

### Running the Application

#### Enhanced API Backend (Current Status)
```bash
# Activate virtual environment first
venv\Scripts\activate  # Windows

# Start the enhanced API
uvicorn backend.src.api.app:app --reload
```

#### Full Stack (After Phase 4)
```bash
python scripts/dev.py
```

### Access Points

- **Enhanced API Backend**: http://localhost:8000
- **Professional API Documentation**: http://localhost:8000/docs (with rich examples)
- **Alternative Documentation**: http://localhost:8000/redoc
- **Frontend**: http://localhost:3000 (Phase 4 - upcoming)

## 📋 Development Phases

### ✅ Phase 1: Web Scraping & Database (Days 1-3) - COMPLETE
- [x] Project setup and structure
- [x] Database schema creation with Turso (LibSQL)
- [x] Playwright-based web scraping implementation
- [x] Data storage and validation (50 KL outlets)
- [x] Comprehensive deduplication and error handling

### ✅ Phase 2: Geocoding Enhancement (Days 4-5) - COMPLETE
- [x] Dual geocoding service integration (Waze + Nominatim)
- [x] Address processing and coordinate retrieval (100% success rate)
- [x] Database updates with geographical data
- [x] GPS coordinate validation for Malaysia bounds

### ✅ Phase 3: Enhanced API Development (Days 6-8) - COMPLETE
- [x] Professional FastAPI endpoints with dependency injection
- [x] Advanced search, filtering, and GPS-based nearby search
- [x] Comprehensive API documentation with examples
- [x] Request logging, response timing, and performance optimization
- [x] Production-ready error handling and validation

### 🎨 Phase 4: Frontend Development (Days 9-12)
- [ ] React/Next.js setup
- [ ] Interactive maps and visualization
- [ ] Responsive UI/UX design
- [ ] API integration

### 🤖 Phase 5: Chatbot Integration (Days 13-15)
- [ ] Chatbot backend development
- [ ] AI integration (OpenAI API)
- [ ] Chat interface frontend
- [ ] Intelligent outlet recommendations

### 🚀 Deployment (Days 16-18)
- [ ] Production deployment to Render
- [ ] Environment configuration
- [ ] Monitoring and maintenance

## 🗄️ Database Schema

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

## 🔑 Environment Variables

Copy `env.example` to `.env` and configure:

```env
# Database
TURSO_DATABASE_URL=your_database_url
TURSO_AUTH_TOKEN=your_auth_token

# Geocoding (choose one)
GOOGLE_MAPS_API_KEY=your_google_api_key
GEOAPIFY_API_KEY=your_geoapify_api_key

# Chatbot
OPENAI_API_KEY=your_openai_api_key

# Development
DEBUG=true
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## 🧪 Testing

```bash
# Backend tests
cd backend
python -m pytest

# Frontend tests (after Phase 4)
cd frontend
npm test

# Integration tests
python scripts/test.py
```

## 📚 API Documentation

Once the backend is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Key API Endpoints (v1)

- `GET /api/v1/` - 🍟 API information and metadata
- `GET /api/v1/health` - 💚 Health check with database status
- `GET /api/v1/outlets` - 🏪 List/search/filter outlets with pagination
- `GET /api/v1/outlets/{id}` - 🏪 Get specific outlet details
- `GET /api/v1/outlets/nearby` - 📍 GPS-based proximity search
- `GET /api/v1/stats` - 📊 Database statistics
- `POST /chat/message` - 🤖 Chatbot interaction (Phase 5)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- McDonald's Malaysia for providing the data source
- OpenStreetMap for geocoding services
- The open-source community for the amazing tools and libraries

## 📞 Support

For questions or issues:
- Create an issue on GitHub
- Check the todo.md for current progress
- Review the API documentation

---

**Status**: ✅ Phase 3 Complete - Enhanced API Ready | 🚧 Phase 4 Next - Frontend Development  
**Current Achievement**: Professional FastAPI backend with 50 KL outlets, advanced search, GPS-based nearby search, and comprehensive documentation  
**Last Updated**: July 2025 