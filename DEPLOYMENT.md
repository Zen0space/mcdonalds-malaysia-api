# Deployment Guide
## McDonald's Malaysia Scraper Project

### 📋 Overview
This guide provides step-by-step instructions for deploying the McDonald's Malaysia Scraper project to production using Render.com.

### 🏗️ Architecture
- **Backend**: FastAPI (Python) deployed as Web Service
- **Frontend**: Next.js deployed as Web Service
- **Database**: Turso (LibSQL) - Cloud hosted
- **Hosting**: Render.com (Free tier compatible)

---

## 🚀 Pre-Deployment Checklist

### ✅ Requirements
- [ ] GitHub repository with latest code
- [ ] Turso database set up and populated
- [ ] Environment variables configured
- [ ] `render.yaml` file in project root
- [ ] Backend and frontend tested locally

### ✅ Accounts Needed
- [ ] GitHub account
- [ ] Render.com account (free tier)
- [ ] Turso account (free tier)

---

## 📦 Project Structure
```
geolocation-mcdscraper/
├── backend/                    # FastAPI backend
│   ├── src/
│   ├── requirements.txt
│   └── main.py
├── frontend/                   # Next.js frontend
│   ├── src/
│   ├── package.json
│   └── next.config.js
├── render.yaml                 # Render deployment config
├── README.md
└── .env.example
```

---

## 🔧 Environment Variables Setup

### Backend Environment Variables
Create these in Render dashboard for backend service:

```env
# Database Configuration
TURSO_DATABASE_URL=https://your-database-url.turso.io
TURSO_AUTH_TOKEN=your_turso_auth_token

# Geocoding Service (FREE)
GEOCODING_PROVIDER=nominatim

# Chatbot Configuration (FREE)
GEMINI_API_KEY=your_gemini_api_key
CHATBOT_PROVIDER=gemini

# Production Configuration
DEBUG=false
LOG_LEVEL=info
```

### Frontend Environment Variables
Create these in Render dashboard for frontend service:

```env
# API Configuration
NEXT_PUBLIC_API_URL=https://your-backend-service.onrender.com

# Map Configuration
NEXT_PUBLIC_MAP_PROVIDER=react-leaflet
NEXT_PUBLIC_MAP_TILES=openstreetmap
```

---

## 🌐 Render.com Deployment

### Step 1: Connect GitHub Repository

1. **Login to Render.com**
   - Go to [render.com](https://render.com)
   - Sign up/login with GitHub

2. **Connect Repository**
   - Click "New" → "Blueprint"
   - Connect your GitHub repository
   - Select `geolocation-mcdscraper` repository

### Step 2: Configure Services

Render will automatically detect the `render.yaml` file and create:

#### Backend Service (`mcd-scraper-api`)
- **Type**: Web Service
- **Environment**: Python
- **Build Command**: `cd backend && pip install -r requirements.txt`
- **Start Command**: `cd backend && python -m uvicorn main:app --host 0.0.0.0 --port $PORT`
- **Plan**: Starter (Free)

#### Frontend Service (`mcd-scraper-frontend`)
- **Type**: Web Service
- **Environment**: Node.js
- **Build Command**: `cd frontend && npm install && npm run build`
- **Start Command**: `cd frontend && npm start`
- **Plan**: Starter (Free)

### Step 3: Set Environment Variables

1. **Backend Service**:
   - Go to service dashboard
   - Click "Environment"
   - Add all backend environment variables

2. **Frontend Service**:
   - Go to service dashboard
   - Click "Environment"
   - Add all frontend environment variables

### Step 4: Deploy

1. **Trigger Deployment**:
   - Render will automatically deploy when you push to main branch
   - Or manually trigger from dashboard

2. **Monitor Deployment**:
   - Check build logs for any errors
   - Wait for both services to be "Live"

---

## 📝 render.yaml Configuration

```yaml
services:
  # FastAPI Backend Service
  - type: web
    name: mcd-scraper-api
    env: python
    buildCommand: "cd backend && pip install -r requirements.txt"
    startCommand: "cd backend && python -m uvicorn main:app --host 0.0.0.0 --port $PORT"
    rootDir: .
    plan: starter
    envVars:
      - key: PYTHON_VERSION
        value: "3.11"
      - key: TURSO_DATABASE_URL
        sync: false
      - key: TURSO_AUTH_TOKEN
        sync: false
      - key: GEOCODING_PROVIDER
        value: "nominatim"
      - key: GEMINI_API_KEY
        sync: false
      - key: CHATBOT_PROVIDER
        value: "gemini"
      - key: DEBUG
        value: "false"
      - key: LOG_LEVEL
        value: "info"

  # Next.js Frontend Service
  - type: web
    name: mcd-scraper-frontend
    env: node
    buildCommand: "cd frontend && npm install && npm run build"
    startCommand: "cd frontend && npm start"
    rootDir: .
    plan: starter
    envVars:
      - key: NEXT_PUBLIC_API_URL
        value: "https://mcd-scraper-api.onrender.com"
      - key: NEXT_PUBLIC_MAP_PROVIDER
        value: "react-leaflet"
      - key: NEXT_PUBLIC_MAP_TILES
        value: "openstreetmap"
```

---

## 🔗 Service URLs

After deployment, you'll get these URLs:

### Backend API
- **URL**: `https://mcd-scraper-api.onrender.com`
- **API Docs**: `https://mcd-scraper-api.onrender.com/docs`
- **Health Check**: `https://mcd-scraper-api.onrender.com/api/v1/health`

### Frontend Application
- **URL**: `https://mcd-scraper-frontend.onrender.com`
- **Map Interface**: Main landing page

---

## 🧪 Post-Deployment Testing

### Backend API Testing
```bash
# Test health endpoint
curl https://mcd-scraper-api.onrender.com/api/v1/health

# Test outlets endpoint
curl https://mcd-scraper-api.onrender.com/api/v1/outlets

# Test nearby search
curl "https://mcd-scraper-api.onrender.com/api/v1/outlets/nearby?lat=3.139&lng=101.6869&radius=5"
```

### Frontend Testing
1. **Load Application**: Visit frontend URL
2. **Check Map**: Verify map loads with outlets
3. **Test Features**: 
   - Outlet markers display
   - Popups work correctly
   - Radius circles show/hide
   - Search functionality
   - Mobile responsiveness

---

## 🔄 Continuous Deployment

### Automatic Deployment
- **Trigger**: Push to `main` branch
- **Process**: Render automatically rebuilds and deploys
- **Duration**: ~5-10 minutes for both services

### Manual Deployment
1. Go to Render dashboard
2. Select service
3. Click "Manual Deploy"
4. Select branch to deploy

---

## 📊 Monitoring & Maintenance

### Health Monitoring
- **Backend**: `/api/v1/health` endpoint
- **Frontend**: Application load time
- **Database**: Connection status in health check

### Logs Access
1. Go to Render dashboard
2. Select service
3. Click "Logs" tab
4. Monitor real-time logs

### Performance Metrics
- **Response Time**: < 2 seconds
- **Uptime**: 99%+ expected
- **Memory Usage**: Monitor in dashboard

---

## 🐛 Troubleshooting

### Common Issues

#### Backend Won't Start
**Symptoms**: Service fails to start, 500 errors
**Solutions**:
- Check Python version (3.11)
- Verify requirements.txt
- Check environment variables
- Review build logs

#### Frontend Build Fails
**Symptoms**: Build process fails, deployment stuck
**Solutions**:
- Check Node.js version compatibility
- Verify package.json
- Check TypeScript errors
- Review build logs

#### Database Connection Issues
**Symptoms**: API returns database errors
**Solutions**:
- Verify Turso URL format (https://)
- Check auth token validity
- Test database connectivity
- Review environment variables

#### CORS Issues
**Symptoms**: Frontend can't connect to backend
**Solutions**:
- Check CORS configuration in FastAPI
- Verify API URL in frontend env vars
- Check service URLs match

### Debug Commands

#### Backend Debugging
```bash
# Check service status
curl https://mcd-scraper-api.onrender.com/api/v1/health

# Test database connection
curl https://mcd-scraper-api.onrender.com/api/v1/stats

# Check API documentation
curl https://mcd-scraper-api.onrender.com/docs
```

#### Frontend Debugging
```bash
# Check build locally
cd frontend
npm run build

# Test production build
npm run start
```

---

## 🔐 Security Considerations

### Environment Variables
- Never commit sensitive data to Git
- Use Render's environment variable system
- Rotate API keys regularly

### CORS Configuration
- Restrict origins in production
- Use HTTPS only
- Validate all inputs

### Rate Limiting
- Implement API rate limiting
- Monitor for abuse
- Use appropriate caching

---

## 📈 Performance Optimization

### Backend Optimization
- Enable response caching
- Use database connection pooling
- Implement request logging
- Monitor response times

### Frontend Optimization
- Enable Next.js optimization
- Use image optimization
- Implement code splitting
- Enable compression

### Database Optimization
- Use appropriate indexes
- Monitor query performance
- Implement connection pooling
- Regular maintenance

---

## 🔄 Backup & Recovery

### Database Backup
- Turso provides automatic backups
- Export data regularly
- Test restore procedures

### Code Backup
- Git repository is primary backup
- Use GitHub's backup features
- Tag releases for rollback

### Configuration Backup
- Document all environment variables
- Keep render.yaml in version control
- Maintain deployment documentation

---

## 📚 Resources

### Documentation
- [Render Documentation](https://render.com/docs)
- [Next.js Deployment](https://nextjs.org/docs/deployment)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)
- [Turso Documentation](https://docs.turso.tech/)

### Support
- [Render Support](https://render.com/support)
- [GitHub Issues](https://github.com/your-repo/issues)
- [Community Forums](https://community.render.com/)

---

## 📞 Emergency Procedures

### Service Down
1. Check Render status page
2. Review service logs
3. Check database connectivity
4. Rollback if necessary

### Critical Bug
1. Identify affected service
2. Revert to previous deployment
3. Fix issue in development
4. Test thoroughly before redeployment

### Data Loss
1. Stop all services
2. Assess data integrity
3. Restore from backup
4. Verify data consistency

---

**Last Updated**: January 2025  
**Version**: 1.0.0  
**Maintainer**: Development Team 