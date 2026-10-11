"""Shared configuration for Groq chat + local FastEmbed embeddings + Chroma."""
import hashlib
import math
import os
import re

from dotenv import load_dotenv
from langchain_core.embeddings import Embeddings

load_dotenv()

# Groq provides the chat/completion model. Embeddings are generated locally because
# Groq's chat API is not an embeddings service.
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "").strip()
MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-20b").strip()
EMBED_PROVIDER = os.getenv("EMBED_PROVIDER", "fastembed").strip().lower()
DB_DIR = os.getenv("DB_DIR", "chroma_db")
COLLECTION = os.getenv("COLLECTION", "college_helpdesk")


def get_model(temperature: float = 0):
    """Create a Groq-hosted chat model using Groq's OpenAI-compatible endpoint."""
    if not GROQ_API_KEY:
        raise SystemExit(
            "GROQ_API_KEY is missing. Copy .env.example to .env and add your Groq API key."
        )

    from langchain_openai import ChatOpenAI

    return ChatOpenAI(
        base_url="https://api.groq.com/openai/v1",
        api_key=GROQ_API_KEY,
        model=MODEL,
        temperature=temperature,
        timeout=60,
        max_retries=2,
    )


class HashEmbeddings(Embeddings):
    """Offline keyword-only fallback. Less semantic than FastEmbed."""
    STOP = set(
        "a an the is are was to of in on for and or by at be it this that "
        "with what how do does i my can".split()
    )

    def _vec(self, text: str):
        v = [0.0] * 256
        for word in re.findall(r"[a-z0-9]+", text.lower()):
            if word in self.STOP:
                continue
            word = word[:-1] if word.endswith("s") and len(word) > 3 else word
            v[int(hashlib.md5(word.encode()).hexdigest(), 16) % 256] += 1.0
        norm = math.sqrt(sum(x * x for x in v)) or 1.0
        return [x / norm for x in v]

    def embed_documents(self, texts):
        return [self._vec(text) for text in texts]

    def embed_query(self, text):
        return self._vec(text)


def get_embeddings():
    """Return local embeddings. No embedding API key or Ollama server is needed."""
    if EMBED_PROVIDER == "fastembed":
        from langchain_community.embeddings import FastEmbedEmbeddings

        return FastEmbedEmbeddings(
            model_name=os.getenv("EMBED_MODEL", "BAAI/bge-small-en-v1.5")
        )
    if EMBED_PROVIDER == "hash":
        return HashEmbeddings()
    raise SystemExit("Unknown EMBED_PROVIDER. Use 'fastembed' or 'hash'.")


def get_vectorstore():
    """Open/create the persistent Chroma vector store."""
    from langchain_chroma import Chroma

    return Chroma(
        collection_name=COLLECTION,
        embedding_function=get_embeddings(),
        persist_directory=DB_DIR,
        collection_metadata={"hnsw:space": "cosine"},
    )
