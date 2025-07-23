# Frontend to Backend API Connection Guide

This guide explains how to connect your McDonald's Malaysia frontend application to the deployed backend API.

## 🔗 Quick Setup

### 1. Update Frontend Environment Variables

In your frontend repository, create or update `.env.local`:

```env
# Development (local backend)
NEXT_PUBLIC_API_URL=http://localhost:8000

# Production (Render backend)
NEXT_PUBLIC_API_URL=https://your-backend-name.onrender.com
```

### 2. Update Backend CORS Settings

In your backend on Render, set the `CORS_ORIGINS` environment variable:

```env
# Development (allow localhost)
CORS_ORIGINS=http://localhost:3000

# Production (your frontend URL)
CORS_ORIGINS=https://your-frontend.vercel.app

# Multiple origins (comma-separated)
CORS_ORIGINS=http://localhost:3000,https://your-frontend.vercel.app
```

## 📋 Step-by-Step Connection Guide

### Step 1: Get Your Backend API URL

After deploying to Render:
1. Go to your Render dashboard
2. Click on your backend service
3. Copy the URL (e.g., `https://mcdonalds-malaysia-api.onrender.com`)

### Step 2: Configure Frontend API Service

Update your frontend's API configuration file (`src/services/api.ts` or similar):

```typescript
// src/services/api.ts
import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000, // 30 seconds (important for Render free tier)
});

// Add response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.code === 'ECONNABORTED') {
      console.error('Request timeout - server may be waking up');
    }
    return Promise.reject(error);
  }
);
```

### Step 3: Update API Endpoints

Ensure all your API calls use the configured base URL:

```typescript
// src/services/outlets.ts
import { api } from './api';

export const outletService = {
  // Get all outlets
  async getOutlets() {
    const response = await api.get('/outlets');
    return response.data;
  },

  // Get specific outlet
  async getOutletById(id: string) {
    const response = await api.get(`/outlets/${id}`);
    return response.data;
  },

  // Search outlets
  async searchOutlets(query: string) {
    const response = await api.get('/outlets/search', {
      params: { q: query }
    });
    return response.data;
  },

  // Get nearby outlets
  async getNearbyOutlets(lat: number, lng: number, radius?: number) {
    const response = await api.get('/outlets/nearby', {
      params: { lat, lng, radius }
    });
    return response.data;
  }
};
```

### Step 4: Update Chat Service

For the AI chatbot integration:

```typescript
// src/services/chat.ts
import { api } from './api';

export const chatService = {
  // Create chat session
  async createSession() {
    const response = await api.post('/chat/sessions');
    return response.data;
  },

  // Send message
  async sendMessage(sessionId: string, message: string) {
    const response = await api.post(`/chat/sessions/${sessionId}/messages`, {
      message
    });
    return response.data;
  }
};
```

## 🌐 CORS Configuration

### Backend CORS Setup

Your backend should already have CORS configured, but verify these settings:

1. **Check Render Environment Variables**
   - Go to Render dashboard → Your service → Environment
   - Ensure `CORS_ORIGINS` is set correctly

2. **Multiple Origins**
   For development and production:
   ```
   CORS_ORIGINS=http://localhost:3000,https://your-frontend.vercel.app
   ```

3. **Wildcard (Development Only)**
   ```
   CORS_ORIGINS=*
   ```
   ⚠️ Never use wildcard in production!

### Frontend Headers

If you need to send custom headers:

```typescript
api.defaults.headers.common['X-Custom-Header'] = 'value';
```

## 🧪 Testing the Connection

### 1. Test Health Endpoint

```typescript
// Quick connection test
async function testConnection() {
  try {
    const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/health`);
    const data = await response.json();
    console.log('API Connection:', data);
  } catch (error) {
    console.error('API Connection Failed:', error);
  }
}
```

### 2. Browser Console Test

Open your frontend and run in browser console:

```javascript
fetch('https://your-backend.onrender.com/health')
  .then(res => res.json())
  .then(data => console.log('API is working:', data))
  .catch(err => console.error('API error:', err));
```

### 3. Network Tab Debugging

1. Open Chrome DevTools → Network tab
2. Make an API request from your frontend
3. Check for:
   - Status code (should be 200)
   - Response headers (check CORS headers)
   - Response time

## ⚠️ Common Issues and Solutions

### Issue 1: CORS Error

**Error**: `Access to fetch at '...' from origin '...' has been blocked by CORS policy`

**Solutions**:
1. Verify `CORS_ORIGINS` in backend includes your frontend URL
2. Check for trailing slashes (remove them)
3. Ensure protocol matches (http vs https)

### Issue 2: Connection Timeout

**Error**: `Network request failed` or timeout errors

**Solutions**:
1. Render free tier sleeps after inactivity - first request may take 30+ seconds
2. Increase timeout in axios configuration
3. Add loading states in UI for slow requests

```typescript
// Handle Render cold starts
const response = await api.get('/outlets', {
  timeout: 60000 // 60 seconds for cold starts
});
```

### Issue 3: 404 Not Found

**Error**: `404 Not Found` on API calls

**Solutions**:
1. Check if API URL has trailing slash
2. Verify endpoint paths match backend routes
3. Check API documentation at `https://your-backend.onrender.com/docs`

### Issue 4: Environment Variables Not Loading

**Solutions**:
1. Restart Next.js development server after changing `.env.local`
2. Ensure variable names start with `NEXT_PUBLIC_`
3. Check for typos in variable names

## 🚀 Production Checklist

Before deploying your frontend:

- [ ] Update `NEXT_PUBLIC_API_URL` to production backend URL
- [ ] Remove any hardcoded localhost URLs
- [ ] Set up proper error handling for API failures
- [ ] Implement retry logic for failed requests
- [ ] Add loading states for all API calls
- [ ] Test all API endpoints with production backend
- [ ] Configure production CORS origins in backend
- [ ] Remove debug console.log statements
- [ ] Set up monitoring/error tracking

## 🔐 Security Considerations

1. **API Keys**
   - Never expose backend API keys in frontend
   - Use environment variables for configuration
   - Implement rate limiting on backend

2. **HTTPS**
   - Always use HTTPS in production
   - Render provides HTTPS by default
   - Ensure frontend is also served over HTTPS

3. **Input Validation**
   - Validate user input on frontend
   - Backend should also validate (never trust frontend)

## 📊 Monitoring the Connection

### Frontend Monitoring

Add connection monitoring:

```typescript
// src/utils/apiMonitor.ts
export const apiMonitor = {
  logRequest: (config: any) => {
    console.log(`API Request: ${config.method?.toUpperCase()} ${config.url}`);
    return config;
  },
  
  logResponse: (response: any) => {
    console.log(`API Response: ${response.status} ${response.config.url}`);
    return response;
  },
  
  logError: (error: any) => {
    console.error(`API Error: ${error.message}`);
    return Promise.reject(error);
  }
};

// Add to axios interceptors
api.interceptors.request.use(apiMonitor.logRequest);
api.interceptors.response.use(apiMonitor.logResponse, apiMonitor.logError);
```

### Health Check Component

Create a component to show API status:

```typescript
// src/components/ApiStatus.tsx
import { useEffect, useState } from 'react';

export function ApiStatus() {
  const [status, setStatus] = useState<'checking' | 'online' | 'offline'>('checking');

  useEffect(() => {
    const checkStatus = async () => {
      try {
        const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/health`);
        setStatus(response.ok ? 'online' : 'offline');
      } catch {
        setStatus('offline');
      }
    };

    checkStatus();
    const interval = setInterval(checkStatus, 60000); // Check every minute
    return () => clearInterval(interval);
  }, []);

  return (
    <div className={`api-status ${status}`}>
      API: {status}
    </div>
  );
}
```

## 🛟 Getting Help

### Debug Information to Collect

When reporting issues, include:

1. **Frontend URL**: Where your frontend is hosted
2. **Backend URL**: Your Render backend URL
3. **Error Messages**: Complete error from browser console
4. **Network Tab**: Screenshot of failed request
5. **CORS Headers**: Response headers from network tab

### Quick Fixes

1. **Clear Browser Cache**: Force refresh with Ctrl+Shift+R
2. **Check API Status**: Visit `https://your-backend.onrender.com/health`
3. **Verify Environment**: Ensure `.env.local` is loaded
4. **Test with Curl**: Test backend directly:
   ```bash
   curl https://your-backend.onrender.com/outlets
   ```

---

**Remember**: 
- Render free tier services sleep after 15 minutes of inactivity
- First request after sleep takes 30+ seconds (show loading state)
- Always test with both local and production backends
- Keep frontend and backend error handling in sync