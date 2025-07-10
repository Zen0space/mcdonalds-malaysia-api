# McDonald's Malaysia Scraper Project

A comprehensive web scraping and data visualization project that extracts McDonald's Malaysia outlet information, adds geocoding, and provides a full-stack web application with chatbot integration.

## 🎯 Project Overview

This project scrapes McDonald's Malaysia outlet data from their official website, enriches it with geographical coordinates, and serves it through a modern web application with visualization and chatbot features.

### Features

- **🕷️ Web Scraping**: Automated scraping of McDonald's Malaysia outlet data
- **🗺️ Geocoding**: Address-to-coordinates conversion for mapping
- **🚀 FastAPI Backend**: RESTful API serving outlet data
- **🎨 React Frontend**: Modern web interface with interactive maps
- **📊 Data Visualization**: Charts and analytics dashboard
- **🤖 Chatbot Integration**: AI-powered outlet recommendations and queries

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

### Backend
- **Python 3.11** - Programming language
- **FastAPI** - Web framework
- **Turso** - SQLite database
- **Playwright/Selenium** - Web scraping
- **Geopy** - Geocoding services
- **OpenAI API** - Chatbot integration

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

#### Backend Only (Current Phase)
```bash
cd backend
py -3.11 -m uvicorn main:app --reload
```

#### Full Stack (After Phase 4)
```bash
python scripts/dev.py
```

### Access Points

- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Frontend**: http://localhost:3000 (after Phase 4)

## 📋 Development Phases

### ✅ Phase 1: Web Scraping & Database (Days 1-3)
- [x] Project setup and structure
- [x] Database schema creation
- [ ] Web scraping implementation
- [ ] Data storage and validation

### 📍 Phase 2: Geocoding Enhancement (Days 4-5)
- [ ] Geocoding service integration
- [ ] Address processing and coordinate retrieval
- [ ] Database updates with geographical data

### 🚀 Phase 3: API Development (Days 6-8)
- [ ] FastAPI endpoints development
- [ ] API documentation
- [ ] Testing and optimization

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

### Key Endpoints

- `GET /outlets` - List all outlets
- `GET /outlets/{id}` - Get specific outlet
- `GET /outlets/search` - Search outlets
- `GET /outlets/nearby` - Find nearby outlets
- `POST /chat/message` - Chatbot interaction

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

**Status**: 🚧 In Development - Phase 1
**Last Updated**: January 2025 