import streamlit as st
import requests
import os
from pathlib import Path

# Configure page
st.set_page_config(
    page_title="RAG Research Assistant",
    page_icon="🔍",
    layout="wide"
)

# API base URL
API_BASE = "http://localhost:8000"

st.title("🔍 RAG Research Assistant")
st.markdown("Upload documents and ask questions about them")

# Sidebar for file upload
with st.sidebar:
    st.header("📁 Upload Documents")
    
    uploaded_file = st.file_uploader(
        "Choose a file",
        type=['txt', 'md', 'pdf'],
        help="Upload text files, markdown, or PDF documents"
    )
    
    if uploaded_file is not None:
        with st.spinner("Processing document..."):
            try:
                # Upload to FastAPI backend
                files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                response = requests.post(f"{API_BASE}/upload", files=files)
                
                if response.status_code == 200:
                    result = response.json()
                    st.success(f"✅ {result['message']}")
                    st.info(f"📊 Created {result['chunks_created']} chunks")
                else:
                    st.error(f"❌ Upload failed: {response.text}")
            except requests.exceptions.ConnectionError:
                st.error("❌ Cannot connect to the backend. Make sure the FastAPI server is running on http://localhost:8000")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    st.header("💬 Ask Questions")
    
    question = st.text_input(
        "Enter your question:",
        placeholder="What would you like to know about your documents?",
        key="question_input"
    )
    
    if st.button("🔍 Search", key="search_button"):
        if question.strip():
            with st.spinner("Searching knowledge base..."):
                try:
                    response = requests.post(
                        f"{API_BASE}/research",
                        json={"question": question}
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        
                        # Display answer
                        st.subheader("📖 Answer")
                        st.write(result["answer"])
                        
                        # Display sources
                        if result["sources"]:
                            st.subheader("📚 Sources")
                            for i, source in enumerate(result["sources"], 1):
                                with st.expander(f"Source {i}: {source['title']} (Score: {source['score']:.2f})"):
                                    st.write(source['content'])
                        else:
                            st.info("ℹ️ No sources found for this answer.")
                    
                    else:
                        st.error(f"❌ Search failed: {response.text}")
                
                except requests.exceptions.ConnectionError:
                    st.error("❌ Cannot connect to the backend. Make sure the FastAPI server is running on http://localhost:8000")
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
        else:
            st.warning("⚠️ Please enter a question.")

with col2:
    st.header("ℹ️ How to Use")
    
    st.markdown("""
    **1. Upload Documents:**
    - Use the file uploader on the left
    - Supported formats: TXT, MD, PDF
    - Documents are automatically processed
    
    **2. Ask Questions:**
    - Type your question in the text box
    - Click "Search" to get answers
    - Answers include source citations
    
    **3. View Sources:**
    - Click on source boxes to see content
    - Scores show relevance to your question
    """)
    
    st.subheader("🚀 Quick Start")
    st.markdown("""
    1. for magarsa repe🐍 :
       ```bash
       we will run ezu also 🤴
       ```
    
    2. Upload some documents
    
    3. Start asking questions!
    """)

# Footer
st.markdown("---")
st.markdown("💡 **Tip:** The more documents you upload, the better the answers will be!")

# Check backend connection
try:
    response = requests.get(f"{API_BASE}/")
    if response.status_code == 200:
        st.success("✅ Backend connected successfully")
    else:
        st.error("❌ Backend connection issue")
except:
    st.error("❌ Backend not running. Start the FastAPI server with: `uvicorn main:app --reload`")
