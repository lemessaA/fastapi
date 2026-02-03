#!/bin/bash

# Frontend Deployment Script
echo "🚀 Deploying RAG Frontend to Render..."

# Create frontend service using curl
curl -X POST "https://api.render.com/v1/services" \
  -H "Authorization: Bearer $RENDER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "web",
    "name": "rag-frontend",
    "ownerId": "$RENDER_OWNER_ID",
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
      }
    ],
    "plan": "free"
  }'

echo "✅ Frontend deployment initiated!"
