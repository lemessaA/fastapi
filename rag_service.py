from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from database import embeddings, collection
import os
from dotenv import load_dotenv
from pathlib import Path
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv(Path(__file__).parent / ".env")

llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0.7, api_key=os.getenv("GROQ_API_KEY"))

def search_research_db(query: str, top_k: int = 3):
    query_embedding = embeddings.embed_query(query)
    results = collection.query(query_embeddings=[query_embedding], n_results=top_k)
    return [
        {
            "content": doc,
            "title": results["metadatas"][0][i].get("title", "Unknown"),
            "score": results["distances"][0][i],
        }
        for i, doc in enumerate(results["documents"][0])
    ]

def answer_research_question(query: str):
    chunks = search_research_db(query)
    if not chunks:
        return ("I don't have enough information to answer this question.", [])

    context = "\n\n".join([f"From {c['title']}:\n{c['content']}" for c in chunks])
    prompt = PromptTemplate(
        input_variables=["context", "question"],
        template="""
Based on the following context document(s), answer the researcher's question:

Research Context:
{context}

Researcher's Question: {question}

Answer: Provide a answer based on the context above.
If the context doesn't contain enough information to fully answer the question, say so clearly.
Only answer based on the provided context, do not make assumptions or provide additional information.
If the question is not related to the context, respond with "I don't have enough information in my
knowledge base to answer this question. Please try adding some documents first.".
Answer clearly and concisely, without unnecessary details.
"""
    ).format(context=context, question=query)
    return llm.invoke(prompt).content, chunks

def ingest_document(file_path: str, original_filename: str):
    """Ingest a single document into the vector database"""
    try:
        # Load the document safely
        documents = safe_load_document(file_path)
        
        # Split into chunks
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=100
        )
        chunks = splitter.split_documents(documents)
        
        # Add to collection
        collection.add(
            documents=[c.page_content for c in chunks],
            metadatas=[
                {
                    "title": original_filename,
                    "chunk": i
                }
                for i in range(len(chunks))
            ],
            ids=[
                f"{original_filename}_{i}"
                for i in range(len(chunks))
            ]
        )
        
        return len(chunks)
    except Exception as e:
        raise Exception(f"Error ingesting document: {str(e)}")

def safe_load_document(filepath):
    """Safely load a document with different encodings and formats"""
    file_extension = os.path.splitext(filepath)[1].lower()
    
    try:
        if file_extension == '.pdf':
            return PyPDFLoader(filepath).load()
        else:
            # Try UTF-8 first, then latin-1 for text files
            try:
                return TextLoader(filepath, encoding='utf-8').load()
            except UnicodeDecodeError:
                return TextLoader(filepath, encoding='latin-1').load()
    except Exception as e:
        raise Exception(f"Error loading document {filepath}: {str(e)}")