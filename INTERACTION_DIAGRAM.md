# 🔄 How Separate Deployments Interact

## Architecture Flow

```
User Browser → Frontend (Streamlit) → Backend (FastAPI) → ChromaDB
     ↓                ↓                    ↓              ↓
  UI Interface   HTTP Requests      API Processing   Vector Storage
```

## 1. File Upload Flow

```
1. User uploads file in Streamlit UI
2. Frontend sends POST to: https://rag-backend.onrender.com/upload
3. Backend processes file and stores in ChromaDB
4. Backend returns success response
5. Frontend shows success message to user
```

## 2. Question Answering Flow

```
1. User asks question in Streamlit UI
2. Frontend sends POST to: https://rag-backend.onrender.com/research
   Body: {"question": "What is FastAPI?", "mode": "research"}
3. Backend searches ChromaDB for relevant documents
4. Backend generates answer using LLM
5. Backend returns JSON with answer and sources
6. Frontend displays answer to user
```

## 3. Environment Configuration

### Frontend Environment Variables
```
BACKEND_URL=https://rag-backend.onrender.com
PORT=8501
STREAMLIT_SERVER_HEADLESS=true
STREAMLIT_SERVER_ADDRESS=0.0.0.0
STREAMLIT_SERVER_PORT=8501
```

### Backend Environment Variables
```
PORT=10000
GROQ_API_KEY=your_api_key_here
```

## 4. API Communication

### Upload Endpoint
```python
# Frontend calls:
response = requests.post(f"{API_BASE}/upload", files=files)

# Backend receives:
@app.post("/upload")
async def upload_file(file: UploadFile = File(...))
```

### Research Endpoint
```python
# Frontend calls:
response = requests.post(f"{API_BASE}/research", 
                        json={"question": question, "mode": mode})

# Backend receives:
@app.post("/research", response_model=ResearchResponse)
async def ask_research_question(request: ResearchRequest)
```

## 5. Data Flow Diagram

```
┌─────────────┐    POST /upload    ┌─────────────┐    Store     ┌─────────────┐
│   User      │ ──────────────────► │  Frontend   │ ───────────► │  Backend    │ ───────────► │ ChromaDB    │
│  Browser    │                    │ (Streamlit) │              │ (FastAPI)   │              │ (Vector DB) │
└─────────────┘                    └─────────────┘              └─────────────┘              └─────────────┘
      │                                   │                            │
      │                                   │                            │
      │         POST /research            │                            │
      └─────────────────────────────────►│                            │
                                          │                            │
                                          │                            │
                                          │  Search & Generate         │
                                          │◄───────────────────────────┘
                                          │
      │                                   │
      │         JSON Response             │
      │◄───────────────────────────────────┘
      │
      │    Display Answer & Sources
      └─────────────────────────────────►
```

## 6. Benefits of Separate Deployment

### Scalability
- Scale frontend and backend independently
- Different resource requirements
- Separate uptime monitoring

### Security
- Backend API can be secured separately
- Frontend can be public-facing
- API key isolation

### Development
- Teams can work independently
- Different deployment cycles
- Separate testing environments

## 7. Troubleshooting

### Common Issues

**CORS Errors**
```python
# Add CORS middleware to backend
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://rag-frontend.onrender.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**Connection Refused**
- Check BACKEND_URL environment variable
- Verify backend is running
- Check network connectivity

**Timeout Issues**
- Render free tier has 15-minute spin-up time
- Implement retry logic in frontend
- Add loading states

## 8. Monitoring

### Health Checks
```bash
# Backend health
curl https://rag-backend.onrender.com/health

# Frontend accessibility
curl https://rag-frontend.onrender.com
```

### Logs
- Check Render dashboard for service logs
- Monitor API response times
- Track error rates
