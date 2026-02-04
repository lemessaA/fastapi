#!/usr/bin/env python3
"""
Unified RAG Application - Single Service Deployment
Combines FastAPI backend and Streamlit frontend in one app
"""

import os
import sys
import threading
import time
import subprocess
import requests
from pathlib import Path

def start_fastapi_backend():
    """Start FastAPI backend in a separate thread"""
    import uvicorn
    from main import app
    
    # Run FastAPI on port 8000 (internal)
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")

def start_streamlit_frontend():
    """Start Streamlit frontend"""
    import streamlit.web.cli as stcli
    
    # Configure Streamlit to use the backend
    os.environ["BACKEND_URL"] = "http://127.0.0.1:8000"
    
    # Streamlit configuration
    sys.argv = [
        "streamlit",
        "run", 
        "streamlit_app.py",
        "--server.port", os.getenv("PORT", "8501"),
        "--server.address", "0.0.0.0",
        "--server.headless", "true",
        "--browser.gatherUsageStats", "false"
    ]
    
    stcli.main()

def wait_for_backend():
    """Wait for backend to be ready"""
    max_wait = 30
    for i in range(max_wait):
        try:
            response = requests.get("http://127.0.0.1:8000/health", timeout=1)
            if response.status_code == 200:
                print("✅ Backend is ready!")
                return True
        except:
            pass
        time.sleep(1)
        print(f"⏳ Waiting for backend... ({i+1}/{max_wait})")
    
    print("❌ Backend failed to start")
    return False

def main():
    """Main application entry point"""
    print("🚀 Starting Unified RAG Application...")
    
    # Start FastAPI backend in background thread
    backend_thread = threading.Thread(target=start_fastapi_backend, daemon=True)
    backend_thread.start()
    
    # Wait for backend to be ready
    if wait_for_backend():
        print("🎯 Starting Streamlit frontend...")
        start_streamlit_frontend()
    else:
        print("❌ Failed to start backend")
        sys.exit(1)

if __name__ == "__main__":
    main()
