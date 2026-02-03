# 🚀 Quick Render Deployment Guide

## Option 1: One-Click Deployment (Easiest)

### Step 1: Deploy Backend
1. Go to: https://render.com/new
2. Click "Web Service"
3. Connect GitHub: Select `lemessaA/fastapi`
4. Configure:
   - **Name**: `rag-backend`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Instance Type**: `Free`
5. Add Environment Variable:
   - `GROQ_API_KEY`: Your Groq API key
6. Click "Create Web Service"

### Step 2: Deploy Frontend
1. Go to: https://render.com/new
2. Click "Web Service"
3. Connect GitHub: Select `lemessaA/fastapi` (same repo)
4. Configure:
   - **Name**: `rag-frontend`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `streamlit run streamlit_app.py --server.port=$PORT --server.address=0.0.0.0 --server.headless=true`
   - **Instance Type**: `Free`
5. Add Environment Variables:
   - `PORT`: `8501`
   - `BACKEND_URL`: `https://rag-backend.onrender.com`
6. Click "Create Web Service"

## Option 2: Using Render.yaml (Advanced)

Your `render.yaml` is already configured. To use it:

1. Push your code to GitHub (already done ✅)
2. In Render Dashboard, click "New" → "Web Service"
3. Connect your repository
4. Render will auto-detect `render.yaml` and create both services

## 🌐 Your URLs After Deployment

- **Backend API**: `https://rag-backend.onrender.com`
- **API Docs**: `https://rag-backend.onrender.com/docs`
- **Frontend UI**: `https://rag-frontend.onrender.com`

## ⚡ Quick Test Commands

```bash
# Test backend health
curl https://rag-backend.onrender.com/health

# Test research endpoint
curl -X POST https://rag-backend.onrender.com/research \
  -H "Content-Type: application/json" \
  -d '{"question": "What is FastAPI?"}'
```

## 🔧 Troubleshooting

If you get port errors:
1. Make sure `PORT` environment variable is set
2. Check that start command uses `$PORT`
3. Wait 2-3 minutes for deployment to complete

## 📋 Deployment Checklist

- [ ] GitHub repo is public and accessible
- [ ] GROQ_API_KEY is set in backend environment
- [ ] BACKEND_URL is set in frontend environment
- [ ] Both services show "Live" status
- [ ] Test the /health endpoint
- [ ] Access the Streamlit UI

**Ready to deploy! Go to https://dashboard.render.com to start.** 🚀
