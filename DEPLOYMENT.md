# 🚀 Deploy to Render

This guide will help you deploy the RAG Research Assistant to Render.com.

## Prerequisites

- Render account (free tier available)
- GitHub repository with the code
- Groq API key

## Step 1: Prepare Your Repository

1. **Push all changes to GitHub:**
```bash
git add .
git commit -m "Add Render deployment configuration"
git push origin main
```

## Step 2: Deploy Backend to Render

1. **Go to [Render Dashboard](https://dashboard.render.com)**
2. **Click "New +" → "Web Service"**
3. **Connect your GitHub repository**
4. **Configure the service:**
   - **Name**: `rag-backend`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Instance Type**: `Free`

5. **Add Environment Variables:**
   - `GROQ_API_KEY`: Your Groq API key
   - `PORT`: `10000`

6. **Click "Create Web Service"**

## Step 3: Deploy Frontend to Render

1. **Create another Web Service**
2. **Configure the frontend:**
   - **Name**: `rag-frontend`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `streamlit run streamlit_app.py --server.port $PORT --server.address 0.0.0.0`
   - **Instance Type**: `Free`

3. **Add Environment Variables:**
   - `BACKEND_URL`: Your backend URL (e.g., `https://rag-backend.onrender.com`)
   - `PORT`: `8501`

## Step 4: Update URLs

After deployment, you'll get URLs like:
- Backend: `https://rag-backend.onrender.com`
- Frontend: `https://rag-frontend.onrender.com`

## Alternative: Single Service Deployment

For simpler deployment, you can deploy just the backend and use the API directly:

1. Deploy only the FastAPI backend
2. Access the interactive docs at: `https://your-app.onrender.com/docs`
3. Use the API endpoints directly

## Important Notes

### Free Tier Limitations
- **15 minutes spin-up time** after inactivity
- **750 hours/month** runtime
- **512MB RAM** limit

### Performance Tips
- Use persistent storage for ChromaDB (consider Render Disk)
- Monitor resource usage
- Consider upgrading to paid tier for production use

### Environment Variables
Never commit API keys to your repository. Always use Render's environment variables.

## Troubleshooting

### Build Fails
- Check `requirements.txt` for correct versions
- Verify all dependencies are compatible

### App Won't Start
- Check the logs in Render dashboard
- Verify start command is correct
- Ensure all environment variables are set

### Connection Issues
- Make sure backend URL is correct in frontend
- Check if both services are running
- Verify CORS settings if needed

## Production Considerations

For production use, consider:
- **Database**: Use managed database for ChromaDB
- **Caching**: Add Redis for better performance
- **Monitoring**: Set up health checks and monitoring
- **Scaling**: Upgrade to paid tiers for better performance
- **Security**: Add authentication and rate limiting

## Cost Estimate

**Free Tier**: $0/month
- Good for development and small projects
- Limited resources and uptime

**Starter ($7/month)**: 
- Better performance
- More resources
- Recommended for small production apps

**Pro ($25/month)**:
- Production-ready performance
- More resources and features
