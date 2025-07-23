# McDonald's Malaysia Location API

A FastAPI backend service that provides McDonald's outlet location data for Malaysia, with geocoding, search, and AI-powered chatbot capabilities.

## 🚀 Features

- **Outlet Data API**: Access McDonald's Malaysia outlet information including locations, operating hours, and services
- **Geocoding**: Convert addresses to coordinates using Nominatim
- **Search**: Find outlets by location, services, or within a radius
- **AI Chatbot**: Natural language queries about McDonald's outlets (Gemini AI integration)
- **Caching**: Efficient response caching for improved performance
- **CORS Support**: Ready for frontend integration

## 🛠️ Tech Stack

- **Framework**: FastAPI (Python 3.9+)
- **Geocoding**: Geopy with Nominatim
- **AI**: Google Gemini API
- **Database**: SQLite (optional PostgreSQL support)
- **Deployment**: Render

## 📋 Prerequisites

- Python 3.9 or higher
- pip package manager
- Google API key (for Gemini chatbot - optional)

## 🔧 Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/geolocation-mcdscrapper.git
cd geolocation-mcdscrapper
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp env.example .env
```

Edit `.env` and configure:
```env
# API Configuration
ENVIRONMENT=development
LOG_LEVEL=info
DEBUG=true

# CORS (set your frontend URL in production)
CORS_ORIGINS=*

# Geocoding
GEOCODING_PROVIDER=nominatim
NOMINATIM_USER_AGENT=mcdonalds-malaysia-api

# Chatbot (optional)
CHATBOT_PROVIDER=gemini
GOOGLE_API_KEY=your_google_api_key_here
```

## 🚀 Running the Application

### Development Mode

```bash
python main.py
```

Or using uvicorn directly:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at: `http://localhost:8000`

### Production Mode

```bash
uvicorn main:app --host 0.0.0.0 --port $PORT
```

## 📚 API Documentation

Once running, access the interactive API documentation:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Main Endpoints

- `GET /health` - Health check
- `GET /outlets` - List all outlets
- `GET /outlets/{id}` - Get specific outlet
- `GET /outlets/search` - Search outlets
- `GET /outlets/nearby` - Find nearby outlets
- `POST /chat` - AI chatbot for outlet queries

## 🌐 Deployment on Render

This project is configured for easy deployment on Render.

1. Push your code to GitHub

2. Create a new Web Service on Render:
   - Connect your GitHub repository
   - Render will auto-detect the `render.yaml` configuration

3. Set environment variables in Render dashboard:
   - `GOOGLE_API_KEY` (if using chatbot)
   - `CORS_ORIGINS` (your frontend URL)

4. Deploy! Render will:
   - Install dependencies from `requirements.txt`
   - Start the server using the configured start command

### Manual Deployment (without render.yaml)

If deploying manually:
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`

## 🗄️ Database Setup (Optional)

For PostgreSQL support:

1. Update `.env`:
```env
DATABASE_URL=postgresql://user:pass@host:port/dbname
```

2. Run migrations:
```bash
python migrate_db.py
```

## 🧪 Running Scripts

### Update Outlet Data
```bash
python scraper_runner.py
```

### Environment Setup Helper
```bash
python setup_env.py
```

## 📁 Project Structure

```
├── src/
│   ├── api/          # FastAPI app and routes
│   ├── chatbot/      # AI chatbot integration
│   ├── database/     # Database models and queries
│   ├── geocoding/    # Geocoding services
│   └── scraper/      # Data scraping utilities
├── scripts/          # Utility scripts
├── main.py          # Application entry point
├── requirements.txt # Python dependencies
├── render.yaml      # Render deployment config
└── README.md        # This file
```

## 🔑 Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `ENVIRONMENT` | Environment mode | No | `development` |
| `LOG_LEVEL` | Logging level | No | `info` |
| `DEBUG` | Debug mode | No | `false` |
| `CORS_ORIGINS` | Allowed CORS origins | No | `*` |
| `GEOCODING_PROVIDER` | Geocoding service | No | `nominatim` |
| `NOMINATIM_USER_AGENT` | User agent for Nominatim | No | `mcdonalds-api` |
| `CHATBOT_PROVIDER` | AI provider | No | `gemini` |
| `GOOGLE_API_KEY` | Google API key for Gemini | No | - |
| `DATABASE_URL` | PostgreSQL connection string | No | - |

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License.

## 🔌 Frontend Integration

For connecting your frontend application to this API, see the [Frontend Connection Guide](FRONTEND_CONNECTION_GUIDE.md).

## 🆘 Support

For issues and questions:
- Open an issue on GitHub
- Check existing issues for solutions
- Review API documentation at `/docs`
