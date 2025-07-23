# McDonald's Malaysia API - Render Deployment Guide

This guide provides step-by-step instructions for deploying the McDonald's Malaysia Location API to Render.

## 🚀 Quick Start

### Prerequisites
- GitHub account with your forked/cloned repository
- Render account (free tier available at [render.com](https://render.com))
- Google API key for Gemini chatbot (optional)

### Automatic Deployment (Recommended)

1. **Push your code to GitHub**
   ```bash
   git add .
   git commit -m "Prepare for Render deployment"
   git push origin main
   ```

2. **Deploy to Render**
   - Go to [Render Dashboard](https://dashboard.render.com/)
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Render will detect the `render.yaml` file automatically
   - Click "Create Web Service"

3. **Configure Environment Variables**
   After deployment, go to your service's Environment tab and add:
   - `GOOGLE_API_KEY` - Your Google API key (if using chatbot)
   - `CORS_ORIGINS` - Your frontend URL (e.g., `https://yourfrontend.vercel.app`)

That's it! Your API will be live at `https://your-service-name.onrender.com`

## 📋 Manual Deployment

If you prefer manual configuration or need to customize settings:

### Step 1: Create New Web Service

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click "New +" → "Web Service"
3. Connect your GitHub account if not already connected
4. Select your repository

### Step 2: Configure Build Settings

Fill in the following settings:

| Setting | Value |
|---------|-------|
| **Name** | `mcdonalds-malaysia-api` (or your preferred name) |
| **Region** | Choose closest to your users |
| **Branch** | `main` (or your default branch) |
| **Root Directory** | Leave blank (uses repository root) |
| **Environment** | `Python 3` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `uvicorn main:app --host 0.0.0.0 --port $PORT` |

### Step 3: Choose Instance Type

- **Free**: Good for testing (512MB RAM, sleeps after inactivity)
- **Starter**: $7/month (512MB RAM, always on)
- **Standard**: $25/month (2GB RAM, better performance)

### Step 4: Set Environment Variables

Add these environment variables:

```bash
# Required for production
ENVIRONMENT=production
LOG_LEVEL=info
DEBUG=false

# CORS Configuration (update with your frontend URL)
CORS_ORIGINS=https://your-frontend-url.com

# Geocoding Service
GEOCODING_PROVIDER=nominatim
NOMINATIM_USER_AGENT=mcdonalds-malaysia-api

# Chatbot Configuration (optional)
CHATBOT_PROVIDER=gemini
GOOGLE_API_KEY=your_google_api_key_here

# Database (optional - for PostgreSQL)
# DATABASE_URL will be automatically set if using Render PostgreSQL
```

### Step 5: Deploy

Click "Create Web Service" and wait for the deployment to complete.

## 🗄️ Database Configuration

### Option 1: SQLite (Default)
The API uses SQLite by default, which is suitable for read-heavy workloads and requires no additional configuration.

### Option 2: PostgreSQL (Recommended for Production)

1. **Create PostgreSQL Database**
   - In Render Dashboard, click "New +" → "PostgreSQL"
   - Choose your plan (free tier available)
   - Create the database

2. **Connect to Your Service**
   - Go to your web service settings
   - Under "Environment", you'll see `DATABASE_URL` automatically added
   - The connection is automatic if both services are in the same Render account

3. **Run Migrations**
   After deployment, use Render Shell:
   ```bash
   python migrate_db.py
   ```

## 🔍 Verifying Deployment

Once deployed, verify your API is working:

1. **Check Health Endpoint**
   ```bash
   curl https://your-service-name.onrender.com/health
   ```

2. **View API Documentation**
   Visit: `https://your-service-name.onrender.com/docs`

3. **Test an API Endpoint**
   ```bash
   curl https://your-service-name.onrender.com/outlets
   ```

## ⚙️ Advanced Configuration

### Custom Domain

1. Go to your service settings
2. Click "Custom Domains"
3. Add your domain
4. Configure DNS as instructed

### Auto-Deploy Configuration

Auto-deploy is enabled by default in `render.yaml`. To modify:

```yaml
services:
  - type: web
    autoDeploy: false  # Set to false to disable
```

### Health Check Configuration

Customize health checks in `render.yaml`:

```yaml
services:
  - type: web
    healthCheckPath: /health
    healthCheckTimeout: 30
    healthCheckMaxRetries: 10
```

### Resource Scaling

To scale your service:

1. Go to service settings
2. Click "Scaling"
3. Adjust instance count or size
4. Save changes

## 🔧 Troubleshooting

### Common Issues and Solutions

#### 1. Build Failures

**Error**: `ModuleNotFoundError`
- **Solution**: Ensure all dependencies are in `requirements.txt`
- Run locally: `pip freeze > requirements.txt`

**Error**: `Python version mismatch`
- **Solution**: Specify Python version in `render.yaml`:
  ```yaml
  envVars:
    - key: PYTHON_VERSION
      value: 3.11
  ```

#### 2. Runtime Errors

**Error**: `Application failed to respond`
- **Check**: Logs for startup errors
- **Verify**: Start command is correct
- **Ensure**: Port binding uses `$PORT` environment variable

**Error**: `CORS errors`
- **Solution**: Update `CORS_ORIGINS` environment variable
- **Note**: Use specific URLs in production, not `*`

#### 3. Database Issues

**Error**: `Database connection failed`
- **Check**: `DATABASE_URL` is set correctly
- **Verify**: Database service is running
- **Solution**: Check connection string format

#### 4. Memory Issues

**Error**: `Out of memory`
- **Solution**: Upgrade to a larger instance
- **Optimize**: Reduce memory usage in code
- **Monitor**: Memory usage in Render dashboard

### Debugging Tips

1. **Enable Debug Mode** (temporarily)
   ```
   DEBUG=true
   LOG_LEVEL=debug
   ```

2. **Check Logs**
   - Go to your service in Render
   - Click "Logs" tab
   - Use search/filter for specific errors

3. **Use Render Shell**
   - Click "Shell" tab in your service
   - Run Python commands directly
   - Test database connections

## 📊 Monitoring

### Metrics Dashboard
- CPU usage
- Memory consumption
- Request count
- Response times

### Setting Up Alerts
1. Go to service settings
2. Click "Notifications"
3. Configure alert thresholds
4. Add notification channels

### Log Management
- Logs are retained for 7 days (free tier)
- Use external log aggregation for longer retention
- Filter logs by level: `error`, `warn`, `info`, `debug`

## 🔄 Continuous Integration

### GitHub Actions Integration

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Render

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to Render
        env:
          RENDER_API_KEY: ${{ secrets.RENDER_API_KEY }}
        run: |
          curl -X POST https://api.render.com/v1/services/${{ secrets.RENDER_SERVICE_ID }}/deploys \
            -H "Authorization: Bearer $RENDER_API_KEY" \
            -H "Content-Type: application/json"
```

### Pre-deployment Testing

Add to your workflow:

```yaml
- name: Run Tests
  run: |
    pip install -r requirements.txt
    python -m pytest tests/
```

## 🔒 Security Best Practices

1. **Environment Variables**
   - Never commit secrets to Git
   - Use Render's secret management
   - Rotate API keys regularly

2. **API Security**
   - Implement rate limiting
   - Use HTTPS (automatic on Render)
   - Validate all inputs

3. **Dependencies**
   - Keep dependencies updated
   - Use `pip audit` for vulnerability scanning
   - Pin versions in `requirements.txt`

## 💰 Cost Optimization

### Free Tier Limitations
- 750 hours/month
- Sleeps after 15 minutes of inactivity
- 512MB RAM
- Shared CPU

### When to Upgrade
- Consistent traffic throughout the day
- Need for background jobs
- Memory requirements > 512MB
- SLA requirements

### Cost-Saving Tips
1. Use caching effectively
2. Optimize database queries
3. Compress responses
4. Use CDN for static assets

## 🆘 Getting Help

### Render Support
- [Documentation](https://render.com/docs)
- [Community Forum](https://community.render.com/)
- [Status Page](https://status.render.com/)
- Email: support@render.com (paid plans)

### Application Support
- Check `/docs` endpoint for API documentation
- Review application logs
- Test endpoints individually
- Use health check endpoint

## 📝 Maintenance Checklist

### Weekly
- [ ] Check error logs
- [ ] Monitor response times
- [ ] Review resource usage

### Monthly
- [ ] Update dependencies
- [ ] Review security alerts
- [ ] Check for Render platform updates
- [ ] Audit environment variables

### Quarterly
- [ ] Performance optimization review
- [ ] Cost analysis
- [ ] Backup verification
- [ ] Security audit

---

**Last Updated**: January 2025  
**Deployment Guide Version**: 1.0.0  

🎉 **Congratulations!** Your McDonald's Malaysia API is now live on Render!