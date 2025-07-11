# McDonald's Malaysia - Interactive Map & Chatbot

A comprehensive full-stack application that provides an interactive map interface and intelligent chatbot for finding McDonald's outlets in Malaysia. Features real-time location detection, outlet search, and AI-powered recommendations.

## 🎯 Project Overview

This project combines web scraping, geocoding, interactive mapping, and AI chatbot technology to create a complete solution for finding McDonald's outlets in Malaysia.

### ✨ Key Features

- **🗺️ Interactive Map**: Leaflet.js powered map with custom McDonald's markers
- **🤖 Intelligent Chatbot**: Gemini 2.5 Flash powered AI assistant
- **📍 Location Services**: Automatic GPS detection and location-based search
- **🔍 Advanced Search**: Find outlets by name, address, or proximity
- **📱 Mobile Responsive**: Optimized for desktop and mobile devices
- **🎨 Modern UI/UX**: Clean design with McDonald's brand colors
- **⚡ Real-time Data**: Live outlet information with operating hours
- **🧭 Navigation**: Direct Waze integration for turn-by-turn directions

## 🏗️ Architecture

**Full-Stack Application Structure**

```
geolocation-mcdscraper/
├── backend/                    # Python FastAPI backend
│   ├── src/
│   │   ├── api/               # REST API endpoints
│   │   ├── chatbot/           # AI chatbot with Gemini
│   │   ├── database/          # SQLite/Turso operations
│   │   ├── scraper/           # Web scraping modules
│   │   └── geocoding/         # Location services
│   ├── main.py                # Backend entry point
│   ├── requirements.txt       # Python dependencies
│   └── README.md             # Backend installation guide
├── frontend/                   # React/Next.js frontend
│   ├── src/
│   │   ├── app/              # Next.js App Router
│   │   ├── components/       # React components
│   │   ├── hooks/            # Custom React hooks
│   │   ├── services/         # API integration
│   │   └── types/            # TypeScript definitions
│   ├── package.json          # Node.js dependencies
│   └── README.md            # Frontend installation guide
├── scripts/                   # Development utilities
├── shared/                    # Shared configurations
├── .env                      # Environment variables (create from env.example)
├── env.example               # Environment template
└── README.md                 # This file - main installation guide
```

## 🚀 Tech Stack

### Backend
- **Python 3.11+** with FastAPI framework
- **Google Gemini 2.5 Flash** for AI chatbot
- **SQLite/Turso** for data storage
- **Playwright** for web scraping
- **Nominatim** for geocoding services

### Frontend
- **React 18** with Next.js 15
- **TypeScript** for type safety
- **Tailwind CSS** for styling
- **Leaflet.js** for interactive maps
- **Custom hooks** for state management

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.8+** (Recommended: Python 3.11+)
- **Node.js 18+** (Recommended: Node.js 20+)
- **npm** or **yarn** package manager
- **Git** for version control
- **Modern web browser** with geolocation support

## 🛠️ Quick Installation Guide

### 1. Clone the Repository
```bash
git clone <repository-url>
cd geolocation-mcdscraper
```

### 2. Environment Setup (Root Directory)
```bash
# Set up environment variables in project root
cp env.example .env

# Edit .env with your configuration
# Required: Add your Gemini API key
# Optional: Add Turso database credentials
```

### 3. Backend Setup
```bash
# Navigate to backend directory
cd backend

# Create and activate virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install

# Run database migration
python migrate_db.py

# Start the backend server
python main.py
```

The backend will be available at:
- **API**: http://localhost:8000
- **Documentation**: http://localhost:8000/docs

### 4. Frontend Setup
```bash
# Open a new terminal and navigate to frontend
cd frontend

# Install Node.js dependencies
npm install

# Set up frontend environment variables
cp env.example .env.local
# Edit .env.local with backend URL (usually no changes needed)

# Start the development server
npm run dev
```

The frontend will be available at:
- **Application**: http://localhost:3000

### 5. Access the Application
1. **Open your browser** to http://localhost:3000
2. **Allow location permissions** when prompted
3. **Explore the map** with McDonald's outlets
4. **Try the chatbot** by clicking the floating chat button
5. **Ask questions** like "Find McDonald's near me"

## 📚 Detailed Installation Guides

For comprehensive setup instructions, troubleshooting, and advanced configuration:

### 🔧 Backend Setup
**📖 [Backend README](backend/README.md)**
- Complete Python environment setup
- Gemini API key configuration
- Database setup and migration
- API endpoint documentation
- Chatbot configuration
- Troubleshooting guide

### 🎨 Frontend Setup
**📖 [Frontend README](frontend/README.md)**
- Node.js environment setup
- React/Next.js configuration
- Map component setup
- Chat interface configuration
- Mobile optimization
- Performance tuning

## 🚀 Development Workflow

### 1. Start Both Services
```bash
# Terminal 1 - Backend
cd backend
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux
python main.py

# Terminal 2 - Frontend
cd frontend
npm run dev
```

### 2. Development URLs
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

### 3. Testing the Integration
1. **Map functionality**: Verify outlets appear on the map
2. **Location services**: Test GPS detection
3. **Chatbot**: Send messages and verify responses
4. **API integration**: Check network requests in browser DevTools

## 🔧 Configuration

### Environment Variables (Root Directory)

#### Main Environment File (`.env`)
```env
# Required for chatbot functionality
GEMINI_API_KEY=your_gemini_api_key_here

# Optional database configuration (uses local SQLite if not provided)
TURSO_DATABASE_URL=your_turso_url_here
TURSO_AUTH_TOKEN=your_turso_token_here

# Optional development settings
DEBUG=true
```

#### Frontend Environment (`.env.local`)
```env
# Required for API communication
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000

# Optional map configuration
NEXT_PUBLIC_MAP_CENTER_LAT=3.1570
NEXT_PUBLIC_MAP_CENTER_LNG=101.7123
```

### Getting API Keys

#### Gemini API Key (Required for Chatbot)
1. Visit [Google AI Studio](https://aistudio.google.com/)
2. Create a new API key
3. Add it to **root directory** `.env` as `GEMINI_API_KEY`

#### Turso Database (Optional - uses local SQLite if not provided)
1. Visit [Turso](https://turso.tech/)
2. Create a database and get URL and auth token
3. Add to **root directory** `.env` as `TURSO_DATABASE_URL` and `TURSO_AUTH_TOKEN`

## 🧪 Testing the Application

### 1. Backend Testing
```bash
cd backend

# Test health endpoint
curl http://localhost:8000/health

# Test outlets endpoint
curl "http://localhost:8000/api/outlets/nearby?lat=3.1570&lng=101.7123"

# Test chat endpoint
curl -X POST "http://localhost:8000/api/chat/sessions" \
  -H "Content-Type: application/json"
```

### 2. Frontend Testing
1. **Open browser** to http://localhost:3000
2. **Check map loading** - verify McDonald's markers appear
3. **Test location services** - allow location permission
4. **Test chatbot** - send a message like "Find McDonald's near me"
5. **Test responsive design** - resize browser window

## 🚨 Common Issues & Solutions

### Environment Issues
- **Missing .env file**: Copy `env.example` to `.env` in **root directory**
- **API key errors**: Verify `GEMINI_API_KEY` in **root directory** `.env`
- **Path issues**: Ensure `.env` is in project root, not backend folder

### Backend Issues
- **Import errors**: Ensure virtual environment is activated
- **Database errors**: Run `python migrate_db.py`
- **Port conflicts**: Backend uses port 8000

### Frontend Issues
- **Build errors**: Run `npm install` and check Node.js version
- **API connection**: Verify `NEXT_PUBLIC_API_BASE_URL` in `frontend/.env.local`
- **Map not loading**: Check browser console for errors
- **Location issues**: Ensure HTTPS or localhost for geolocation

### Integration Issues
- **CORS errors**: Backend has CORS configured for localhost:3000
- **Chat not working**: Ensure backend is running and accessible
- **No outlet data**: Check if database has been populated

## 🔄 Development Scripts

### Backend Scripts
```bash
cd backend
python main.py              # Start development server
python migrate_db.py        # Run database migration
python -m pytest           # Run tests (if available)
```

### Frontend Scripts
```bash
cd frontend
npm run dev                 # Start development server
npm run build              # Build for production
npm run start              # Start production server
npm run lint               # Check code quality
npm run type-check         # TypeScript validation
```

## 📊 Project Status

### ✅ Completed Features
- **Backend API**: Complete with all endpoints
- **Database**: SQLite with migration support
- **Chatbot**: Gemini 2.5 Flash integration
- **Frontend**: React/Next.js application
- **Map Interface**: Interactive Leaflet map
- **Location Services**: GPS integration
- **Chat Interface**: Real-time messaging
- **Mobile Support**: Responsive design

### 🚧 Future Enhancements
- **Offline Support**: PWA capabilities
- **Advanced Analytics**: Usage statistics
- **Multi-language**: Bahasa Malaysia support
- **Push Notifications**: Real-time updates
- **Social Features**: Share locations

## 🤝 Contributing

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/new-feature`
3. **Follow the development workflow**
4. **Test thoroughly** on both frontend and backend
5. **Submit a pull request**

### Development Guidelines
- **Backend**: Follow Python PEP 8 style guide
- **Frontend**: Use TypeScript and ESLint rules
- **Testing**: Test all API integrations
- **Documentation**: Update READMEs for new features

## 📞 Support

### Getting Help
1. **Check the detailed READMEs**:
   - [Backend README](backend/README.md) for API issues
   - [Frontend README](frontend/README.md) for UI issues
2. **Check browser console** for error messages
3. **Verify environment variables** are set correctly in **root directory**
4. **Ensure both services are running** on correct ports

### Troubleshooting Resources
- **Backend logs**: Check terminal output when running `python main.py`
- **Frontend logs**: Check browser DevTools console
- **API testing**: Use http://localhost:8000/docs for interactive testing
- **Network issues**: Check browser Network tab for failed requests

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🎉 Ready to Explore!

Once both services are running:

1. **🗺️ Explore the Map**: View all McDonald's outlets in Malaysia
2. **📍 Use Location Services**: Find outlets near your current location
3. **🤖 Chat with AI**: Ask questions like "Find McDonald's in KLCC"
4. **🧭 Get Directions**: Click Waze buttons for turn-by-turn navigation
5. **📱 Try Mobile**: Test on your phone for the full experience

**Happy exploring! 🍟🚀** 