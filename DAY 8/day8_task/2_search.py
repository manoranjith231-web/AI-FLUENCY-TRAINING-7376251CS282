"""Try handbook questions and print similarity distances for threshold selection."""
from lc_config import get_vector_store, MAX_DISTANCE

QUESTIONS = [
    "What CGPA do I need to be eligible for placements?",
    "What is the capital of France?",
]

def main():
    store = get_vector_store()
    for query in QUESTIONS:
        print("\n" + "=" * 72)
        print("QUESTION:", query)
        results = store.similarity_search_with_score(query, k=3)
        if not results:
            print("No search results.")
            continue
        for rank, (doc, score) in enumerate(results, start=1):
            print(
                f"{rank}. source={doc.metadata.get('source', 'unknown')} "
                f"distance={score:.4f}"
            )
            print(doc.page_content[:300].replace("\n", " "))
        print("Current MAX_DISTANCE:", MAX_DISTANCE)
        print("Chunks retained:", sum(1 for _, score in results if score <= MAX_DISTANCE))

if __name__ == "__main__":
    main()
