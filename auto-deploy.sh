#!/bin/bash

echo "🚀 Starting Automated Render Deployment..."

# Check if we have the necessary environment variables
if [ -z "$RENDER_API_KEY" ]; then
    echo "❌ RENDER_API_KEY not found. Please set it first."
    echo "Get your API key from: https://dashboard.render.com/user/settings"
    exit 1
fi

echo "✅ API Key found. Creating backend service..."

# Create Backend Service
BACKEND_RESPONSE=$(curl -s -X POST "https://api.render.com/v1/services" \
  -H "Authorization: Bearer $RENDER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "web",
    "name": "rag-backend",
    "repo": "https://github.com/lemessaA/fastapi.git",
    "branch": "main",
    "runtime": "python",
    "buildCommand": "pip install -r requirements.txt",
    "startCommand": "uvicorn main:app --host 0.0.0.0 --port $PORT",
    "envVars": [
      {
        "key": "PORT",
        "value": "10000"
      }
    ],
    "plan": "free"
  }')

echo "Backend Response: $BACKEND_RESPONSE"

# Wait a moment before creating frontend
sleep 5

echo "✅ Creating frontend service..."

# Create Frontend Service
FRONTEND_RESPONSE=$(curl -s -X POST "https://api.render.com/v1/services" \
  -H "Authorization: Bearer $RENDER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "web",
    "name": "rag-frontend",
    "repo": "https://github.com/lemessaA/fastapi.git",
    "branch": "main",
    "runtime": "python",
    "buildCommand": "pip install -r requirements.txt",
    "startCommand": "streamlit run streamlit_app.py --server.port=$PORT --server.address=0.0.0.0 --server.headless=true",
    "envVars": [
      {
        "key": "PORT",
        "value": "8501"
      },
      {
        "key": "BACKEND_URL",
        "value": "https://rag-backend.onrender.com"
      },
      {
        "key": "STREAMLIT_SERVER_HEADLESS",
        "value": "true"
      },
      {
        "key": "STREAMLIT_SERVER_ADDRESS",
        "value": "0.0.0.0"
      },
      {
        "key": "STREAMLIT_SERVER_PORT",
        "value": "8501"
      }
    ],
    "plan": "free"
  }')

echo "Frontend Response: $FRONTEND_RESPONSE"

echo "🎉 Deployment initiated! Check your Render Dashboard for progress."
echo "📊 Dashboard: https://dashboard.render.com"
echo "🌐 Your URLs will be:"
echo "   Backend: https://rag-backend.onrender.com"
echo "   Frontend: https://rag-frontend.onrender.com"
