"""Search the Chroma vector store without calling a chat LLM."""
from lc_config import get_vectorstore


def main():
    store = get_vectorstore()
    questions = [
        "How much is the late fee for paying fees after the due date?",
        "What time should hostel students return?",
        "Can I write the exam with 70% attendance?",
    ]

    for question in questions:
        print(f"\nQ: {question}")
        # Cosine distance: smaller generally means more similar.
        for doc, score in store.similarity_search_with_score(question, k=3):
            print(
                f"  {score:.3f}  [{doc.metadata.get('source', 'unknown')}] "
                f"{doc.page_content[:100]!r}"
            )

    print("\nFiltered to library.md:")
    for doc in store.similarity_search(
        "fine for late return", k=2, filter={"source": "library.md"}
    ):
        print("  ", doc.metadata.get("source", "unknown"), "->",
              doc.page_content[:100].replace("\n", " "))


if __name__ == "__main__":
    main()
