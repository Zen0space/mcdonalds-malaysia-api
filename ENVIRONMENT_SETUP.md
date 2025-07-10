# Environment Setup Guide

## 🚨 Important: Avoiding Package Conflicts

This project uses a **virtual environment** to isolate dependencies and avoid conflicts with your global Python installation.

### ⚠️ Common Issues

If you see warnings about "packages installed in root" or conflicts, it means packages are being installed globally instead of in the virtual environment.

### ✅ Correct Setup

1. **Always activate the virtual environment first:**
   ```bash
   # Windows
   venv\Scripts\activate
   
   # You should see (venv) in your prompt:
   (venv) PS E:\Github\geolocation-mcdscraper>
   ```

2. **Check your environment:**
   ```bash
   python scripts/activate_env.py
   ```

3. **Install packages only in the virtual environment:**
   ```bash
   # Make sure (venv) is in your prompt first!
   pip install package_name
   ```

### 🔧 Environment Management Commands

```bash
# Create virtual environment (only needed once)
py -3.11 -m venv venv

# Activate virtual environment (needed every time)
venv\Scripts\activate

# Deactivate virtual environment
deactivate

# Check environment status
python scripts/activate_env.py

# Install project dependencies
pip install -r backend/requirements.txt
```

### 🏗️ Project Structure

```
geolocation-mcdscraper/
├── venv/                    # Virtual environment (isolated)
├── backend/                 # Python backend code
│   ├── requirements.txt     # Backend dependencies
│   └── src/                 # Source code
├── frontend/                # React frontend
│   └── package.json         # Frontend dependencies
└── scripts/                 # Helper scripts
    └── activate_env.py      # Environment checker
```

### 📦 Dependencies

**Backend (Python):**
- playwright (web scraping)
- beautifulsoup4 (HTML parsing)
- requests (HTTP requests)
- libsql-client (Turso database)
- pandas (data manipulation)
- python-dotenv (environment variables)

**Frontend (Node.js):**
- Next.js (React framework)
- TypeScript (type safety)
- React Leaflet (maps)
- Chart.js (visualization)

### 🐛 Troubleshooting

**Problem:** "Package installed in root" warning
**Solution:** Make sure virtual environment is activated (`venv\Scripts\activate`)

**Problem:** Import errors
**Solution:** Check environment with `python scripts/activate_env.py`

**Problem:** Global packages interfering
**Solution:** Use virtual environment exclusively for this project

### 🎯 Best Practices

1. **Always activate virtual environment** before working
2. **Never install packages globally** for this project
3. **Use the environment checker** to verify setup
4. **Keep dependencies in requirements.txt** updated
5. **Use separate environments** for different projects

### 📋 Quick Start Checklist

- [ ] Virtual environment created: `py -3.11 -m venv venv`
- [ ] Virtual environment activated: `venv\Scripts\activate`
- [ ] Environment verified: `python scripts/activate_env.py`
- [ ] Dependencies installed: `pip install -r backend/requirements.txt`
- [ ] Ready to develop! 🚀 