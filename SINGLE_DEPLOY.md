# 🚀 Single Service Deployment

## Deploy Everything in One Frontend Service

This approach deploys both FastAPI backend and Streamlit frontend in a single Render service.

### Why Single Service?
- ✅ **Simpler**: Only one service to manage
- ✅ **No CORS issues**: Backend and frontend run together
- ✅ **Free tier friendly**: Uses only one service
- ✅ **Easier debugging**: Everything in one place

### Architecture
```
┌─────────────────────────────────────┐
│         Render Service              │
│  ┌─────────────┐  ┌─────────────┐  │
│  │   Streamlit │  │   FastAPI   │  │
│  │  Frontend   │  │   Backend   │  │
│  │   :8501     │  │   :8000     │  │
│  └─────────────┘  └─────────────┘  │
│         ↓                           │
│      ChromaDB                       │
└─────────────────────────────────────┘
```

## Quick Deploy

### Step 1: Deploy Single Service
**Click this link:** https://render.com/new?repo=https://github.com/lemessaA/fastapi.git

**Configure:**
- **Name**: `rag-app`
- **Runtime**: `Python 3`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `python app.py`
- **Instance Type**: `Free`
- **Environment Variables**:
  - `PORT`: `8501`
  - `GROQ_API_KEY`: Your Groq API key
  - `PYTHONUNBUFFERED`: `1`

### Step 2: Wait for Deployment
- Build takes ~2-3 minutes
- Backend starts first (port 8000)
- Frontend starts next (port 8501)
- Your app will be available at: `https://rag-app.onrender.com`

## How It Works

### app.py (Unified Launcher)
```python
# 1. Starts FastAPI backend on port 8000 (internal)
# 2. Waits for backend to be ready
# 3. Starts Streamlit frontend on port 8501 (external)
# 4. Streamlit connects to backend via http://127.0.0.1:8000
```

### Internal Communication
- **Backend**: `http://127.0.0.1:8000` (internal only)
- **Frontend**: `https://rag-app.onrender.com` (external)
- **API Calls**: Streamlit → Backend (localhost)

## Testing

### Health Check
```bash
curl https://rag-app.onrender.com
```

### API Test
```bash
curl -X POST https://rag-app.onrender.com/research \
  -H "Content-Type: application/json" \
  -d '{"question": "What is FastAPI?", "mode": "research"}'
```

## Benefits

### ✅ Advantages
- **Single Service**: Easier to manage
- **No CORS**: Internal communication
- **Free Tier**: Only one service needed
- **Simple Setup**: Less configuration

### ⚠️ Limitations
- **Scaling**: Backend and frontend scale together
- **Resources**: Shared memory/CPU
- **Debugging**: Logs mixed together

## Troubleshooting

### Backend Not Ready
If you see "Backend failed to start":
1. Check the logs in Render dashboard
2. Verify GROQ_API_KEY is set correctly
3. Check for import errors

### Frontend Issues
If Streamlit doesn't start:
1. Check if port 8501 is available
2. Verify streamlit dependencies
3. Check for syntax errors

### Connection Issues
If frontend can't reach backend:
1. Wait a bit longer for backend startup
2. Check if backend is running on 127.0.0.1:8000
3. Review the startup logs

## Files Used

- `app.py` - Unified application launcher
- `render-single.yaml` - Single service configuration
- `Procfile.single` - Single service Procfile
- `streamlit_app.py` - Updated for local backend
- `main.py` - FastAPI backend (unchanged)

## Ready to Deploy! 🚀

**Click here to deploy:** https://render.com/new?repo=https://github.com/lemessaA/fastapi.git

Your unified RAG application will be available at: `https://rag-app.onrender.com`
