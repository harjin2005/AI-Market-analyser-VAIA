"""Configuration settings for the AI Market Analyst using Groq and HuggingFace."""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Application configuration."""
    
    # Groq Configuration
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    GROQ_MODEL = os.getenv("GROQ_MODEL", "mixtral-8x7b-32768")
    
    # Embedding Configuration (HuggingFace - Free!)
    EMBEDDING_MODEL_TYPE = os.getenv("EMBEDDING_MODEL_TYPE", "huggingface")
    EMBEDDING_MODEL_NAME = os.getenv("EMBEDDING_MODEL_NAME", "sentence-transformers/all-MiniLM-L6-v2")
    
    # Vector DB Configuration
    VECTOR_DB_PATH = os.getenv("VECTOR_DB_PATH", "./chroma_db")
    COLLECTION_NAME = os.getenv("COLLECTION_NAME", "innovate_inc_docs")
    
    # Chunking Configuration
    CHUNK_SIZE = 500
    CHUNK_OVERLAP = 100
    
    # Document Path
    DOCUMENT_PATH = "innovate_inc_report.txt"
    
    # API Configuration
    API_HOST = "0.0.0.0"
    API_PORT = 8000

config = Config()
