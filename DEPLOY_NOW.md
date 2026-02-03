# 🚀 DEPLOY NOW - Click These Links

## Step 1: Deploy Backend
**Click this link:** https://render.com/new?repo=https://github.com/lemessaA/fastapi.git

Then configure:
- **Name**: `rag-backend`
- **Runtime**: `Python 3`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
- **Instance Type**: `Free`
- **Environment Variables**:
  - `GROQ_API_KEY`: Your Groq API key

## Step 2: Deploy Frontend
**Click this link:** https://render.com/new?repo=https://github.com/lemessaA/fastapi.git

Then configure:
- **Name**: `rag-frontend`
- **Runtime**: `Python 3`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `streamlit run streamlit_app.py --server.port=$PORT --server.address=0.0.0.0 --server.headless=true`
- **Instance Type**: `Free`
- **Environment Variables**:
  - `PORT`: `8501`
  - `BACKEND_URL`: `https://rag-backend.onrender.com`
  - `STREAMLIT_SERVER_HEADLESS`: `true`
  - `STREAMLIT_SERVER_ADDRESS`: `0.0.0.0`
  - `STREAMLIT_SERVER_PORT`: `8501`

## 🎯 After Deployment

Your URLs will be:
- **API**: https://rag-backend.onrender.com
- **API Docs**: https://rag-backend.onrender.com/docs
- **Frontend**: https://rag-frontend.onrender.com

## ⚡ Quick Test

```bash
# Test backend
curl https://rag-backend.onrender.com/health

# Test API
curl -X POST https://rag-backend.onrender.com/research \
  -H "Content-Type: application/json" \
  -d '{"question": "What is FastAPI?", "mode": "research"}'
```

**Ready! Click the links above to deploy!** 🚀
