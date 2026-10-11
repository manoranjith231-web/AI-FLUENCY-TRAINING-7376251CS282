"""Load the six Markdown handbook files and index their chunks in Chroma."""
from pathlib import Path
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from lc_config import DATA_DIR, CHROMA_DIR, COLLECTION_NAME, get_embeddings

def main():
    data_path = Path(DATA_DIR)
    if not data_path.exists():
        raise FileNotFoundError(f"Data folder not found: {data_path.resolve()}")

    paths = sorted(data_path.glob("*.md"))
    if not paths:
        raise FileNotFoundError("No .md files found inside the data folder.")

    documents = []
    for path in paths:
        loader = TextLoader(str(path), encoding="utf-8")
        loaded = loader.load()
        for doc in loaded:
            doc.metadata["source"] = path.name
        documents.extend(loaded)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=700,
        chunk_overlap=100,
        separators=["\n## ", "\n### ", "\n", " ", ""],
    )
    chunks = splitter.split_documents(documents)

    # Rebuild the collection so rerunning ingestion does not duplicate chunks.
    import shutil
    chroma_path = Path(CHROMA_DIR)
    if chroma_path.exists():
        shutil.rmtree(chroma_path)

    store = Chroma.from_documents(
        documents=chunks,
        embedding=get_embeddings(),
        collection_name=COLLECTION_NAME,
        persist_directory=CHROMA_DIR,
        collection_metadata={"hnsw:space": "cosine"},
    )

    print(f"Documents loaded: {len(paths)}")
    print(f"Chunks created: {len(chunks)}")
    print(f"Vector database saved to: {chroma_path.resolve()}")

if __name__ == "__main__":
    main()
