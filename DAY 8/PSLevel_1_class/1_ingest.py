"""Load Markdown files from data/, chunk them, embed locally, and store in Chroma."""
import shutil
from pathlib import Path

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from lc_config import DB_DIR, EMBED_PROVIDER, get_embeddings, get_vectorstore

DATA_DIR = Path("data")


def main():
    paths = sorted(DATA_DIR.glob("*.md"))
    if not paths:
        raise SystemExit(
            f"No .md files found in {DATA_DIR.resolve()}. Add your handbook Markdown files there."
        )

    docs = [
        Document(
            page_content=path.read_text(encoding="utf-8"),
            metadata={"source": path.name},
        )
        for path in paths
    ]
    print(f"Loaded {len(docs)} documents")

    splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=50)
    chunks = splitter.split_documents(docs)
    if not chunks:
        raise SystemExit("No text chunks were created. Check that your Markdown files are not empty.")

    print(f"Split into {len(chunks)} chunks (chunk_size=300, overlap=50)")
    print("Example chunk ->", repr(chunks[0].page_content[:120]), chunks[0].metadata)

    # Remove the old database to prevent duplicate vectors on a fresh ingestion.
    shutil.rmtree(DB_DIR, ignore_errors=True)
    store = get_vectorstore()
    ids = store.add_documents(chunks)

    print(f"Stored {len(ids)} vectors in ./{DB_DIR} using EMBED_PROVIDER={EMBED_PROVIDER}")
    print("Vector length:", len(get_embeddings().embed_query("test")))


if __name__ == "__main__":
    main()
