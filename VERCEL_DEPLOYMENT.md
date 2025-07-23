# Vercel Deployment Guide for McDonald's Scraper

This guide will help you deploy your monorepo (FastAPI backend + Next.js frontend) to Vercel for free.

## Prerequisites

1. A Vercel account (sign up at https://vercel.com)
2. GitHub repository with your code
3. Environment variables ready (Turso database credentials, API keys)

## Project Structure Requirements

Your project structure should look like this:
```
geolocation-mcdscrapper/
├── api/                    # Vercel serverless functions
│   ├── index.py           # FastAPI entry point
│   └── requirements.txt   # Python dependencies
├── backend/               # Original backend code
│   └── src/
├── frontend/              # Next.js application
│   ├── package.json
│   └── ...
├── vercel.json           # Vercel configuration
└── .vercelignore         # Files to ignore during deployment
```

## Step-by-Step Deployment

### 1. Prepare Your Repository

Ensure all the required files are committed to your GitHub repository:
- `vercel.json` - Vercel configuration
- `api/index.py` - FastAPI entry point
- `api/requirements.txt` - Python dependencies
- `.vercelignore` - Deployment exclusions

### 2. Connect to Vercel

1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Click "Add New Project"
3. Import your GitHub repository
4. Select your `geolocation-mcdscrapper` repository

### 3. Configure Build Settings

Vercel should automatically detect the configuration from `vercel.json`, but verify:

- **Framework Preset**: Next.js
- **Root Directory**: Leave empty (we're using a monorepo)
- **Build Command**: `cd frontend && npm install && npm run build`
- **Output Directory**: `frontend/.next`
- **Install Command**: `cd frontend && npm install`

### 4. Set Environment Variables

In the Vercel dashboard, add these environment variables:

#### Required Variables:
```
TURSO_DATABASE_URL=your_turso_database_url
TURSO_AUTH_TOKEN=your_turso_auth_token
GEMINI_API_KEY=your_gemini_api_key
```

#### Optional Variables (already set in vercel.json):
```
NEXT_PUBLIC_MAP_PROVIDER=react-leaflet
NEXT_PUBLIC_MAP_TILES=openstreetmap
GEOCODING_PROVIDER=nominatim
CHATBOT_PROVIDER=gemini
DEBUG=false
LOG_LEVEL=info
```

### 5. Deploy

Click "Deploy" and wait for the deployment to complete. Vercel will:
- Build your Next.js frontend
- Set up Python serverless functions for your FastAPI backend
- Configure routing between frontend and backend

## Post-Deployment

### Access Your Application

- **Frontend**: `https://your-project-name.vercel.app`
- **API**: `https://your-project-name.vercel.app/api`
- **API Docs**: `https://your-project-name.vercel.app/api/docs`

### Test Endpoints

1. Health Check:
   ```bash
   curl https://your-project-name.vercel.app/api/health
   ```

2. Outlets Endpoint:
   ```bash
   curl https://your-project-name.vercel.app/api/outlets
   ```

## Important Notes

### Serverless Function Limitations (Free Tier)

- **Timeout**: 10 seconds max per request
- **Memory**: 512 MB
- **Region**: Singapore (sin1) for better performance in Malaysia
- **Cold Starts**: First request may be slower

### Backend Adjustments

The FastAPI app runs as serverless functions, which means:
- No background tasks
- No WebSocket support (on free tier)
- Each request is stateless
- Database connections should be lightweight

### Troubleshooting

1. **Import Errors**: Check the Vercel function logs for missing dependencies
2. **CORS Issues**: The `api/index.py` includes CORS configuration
3. **Environment Variables**: Ensure all required variables are set in Vercel dashboard
4. **Build Failures**: Check if Python version (3.12) is compatible with all dependencies

### Monitoring

- View logs: Vercel Dashboard → Functions → Logs
- Check build output: Vercel Dashboard → Deployments → Build Logs
- Monitor usage: Vercel Dashboard → Usage

## Alternative Deployment Strategy

If you encounter issues with the monorepo setup, you can deploy frontend and backend separately:

1. **Frontend on Vercel**: Deploy only the frontend folder
2. **Backend on Fly.io/Railway**: Deploy the backend separately
3. Update `NEXT_PUBLIC_API_URL` to point to your backend URL

## Updating Your Deployment

To update your deployment:
1. Push changes to your GitHub repository
2. Vercel automatically triggers a new deployment
3. Monitor the deployment in the Vercel dashboard

## Cost Considerations

Vercel's free tier includes:
- 100 GB bandwidth per month
- 100,000 serverless function invocations
- 100 hours of function execution time
- Unlimited static site hosting

This should be sufficient for most small to medium projects.

## Support

- Vercel Documentation: https://vercel.com/docs
- FastAPI on Vercel: https://vercel.com/templates/python/fastapi
- Next.js on Vercel: https://vercel.com/docs/frameworks/nextjs