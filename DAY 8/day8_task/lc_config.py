"""Shared configuration for the Day 8 College Helpdesk RAG project."""
import os
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq

load_dotenv()

DATA_DIR = "data"
CHROMA_DIR = "chroma_db"
COLLECTION_NAME = "college_handbook"
MAX_DISTANCE = float(os.getenv("MAX_DISTANCE", "0.6"))
EMBEDDING_MODEL = os.getenv(
    "EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2"
)
LLM_MODEL = os.getenv("LLM_MODEL", "llama-3.3-70b-versatile")


def get_embeddings():
    """Create the same embedding model for ingestion and searching."""
    return HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)


def get_vector_store():
    """Open the existing persistent Chroma collection."""
    from langchain_chroma import Chroma

    return Chroma(
        collection_name=COLLECTION_NAME,
        persist_directory=CHROMA_DIR,
        embedding_function=get_embeddings(),
        collection_metadata={"hnsw:space": "cosine"},
    )


def get_llm():
    """Create the configured Groq chat model."""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key or api_key == "your_groq_api_key_here":
        raise RuntimeError(
            "GROQ_API_KEY is missing. Copy .env.example to .env and add your Groq API key."
        )
    return ChatGroq(model=LLM_MODEL, temperature=0)
