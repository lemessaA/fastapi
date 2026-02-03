#!/bin/bash

# Backend Deployment Script
echo "🚀 Deploying RAG Backend to Render..."

# Create backend service using curl
curl -X POST "https://api.render.com/v1/services" \
  -H "Authorization: Bearer $RENDER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "web",
    "name": "rag-backend",
    "ownerId": "$RENDER_OWNER_ID",
    "repo": "https://github.com/lemessaA/fastapi.git",
    "branch": "main",
    "runtime": "python",
    "buildCommand": "pip install -r requirements.txt",
    "startCommand": "uvicorn main:app --host 0.0.0.0 --port $PORT",
    "envVars": [
      {
        "key": "PORT",
        "value": "10000"
      },
      {
        "key": "GROQ_API_KEY",
        "value": "'$GROQ_API_KEY'"
      }
    ],
    "plan": "free"
  }'

echo "✅ Backend deployment initiated!"
