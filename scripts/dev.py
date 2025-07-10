#!/usr/bin/env python3
"""
Development script to run both backend and frontend servers
"""

import subprocess
import sys
import os
import time
import signal
from pathlib import Path

def run_backend():
    """Run the FastAPI backend server"""
    print("🚀 Starting FastAPI backend server...")
    backend_dir = Path(__file__).parent.parent / "backend"
    os.chdir(backend_dir)
    
    # Run with Python 3.11
    return subprocess.Popen([
        "py", "-3.11", "-m", "uvicorn", "main:app", 
        "--reload", "--host", "0.0.0.0", "--port", "8000"
    ])

def run_frontend():
    """Run the React/Next.js frontend server"""
    print("🎨 Starting React frontend server...")
    frontend_dir = Path(__file__).parent.parent / "frontend"
    
    if not frontend_dir.exists():
        print("⚠️  Frontend directory not found. Run Phase 4 setup first.")
        return None
    
    os.chdir(frontend_dir)
    
    # Check if package.json exists
    if not (frontend_dir / "package.json").exists():
        print("⚠️  Frontend not initialized. Run Phase 4 setup first.")
        return None
    
    return subprocess.Popen(["npm", "run", "dev"])

def main():
    """Main function to run both servers"""
    print("🔧 McDonald's Scraper Development Server")
    print("=" * 50)
    
    processes = []
    
    try:
        # Start backend
        backend_process = run_backend()
        if backend_process:
            processes.append(backend_process)
            time.sleep(2)  # Give backend time to start
        
        # Start frontend (if available)
        frontend_process = run_frontend()
        if frontend_process:
            processes.append(frontend_process)
        
        print("\n✅ Development servers started!")
        print("🔗 Backend API: http://localhost:8000")
        print("📚 API Docs: http://localhost:8000/docs")
        if frontend_process:
            print("🎨 Frontend: http://localhost:3000")
        
        print("\n⌨️  Press Ctrl+C to stop all servers")
        
        # Wait for processes
        for process in processes:
            process.wait()
            
    except KeyboardInterrupt:
        print("\n🛑 Stopping development servers...")
        
        # Terminate all processes
        for process in processes:
            if process.poll() is None:  # Process is still running
                process.terminate()
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    process.kill()
        
        print("✅ All servers stopped")
        sys.exit(0)
    
    except Exception as e:
        print(f"❌ Error starting servers: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 