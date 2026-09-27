from src.retrieval.semantic import (
    SemanticRetriever,
)


retriever = SemanticRetriever()


queries = [
    "How are tasks created?",
    "Which model validates tasks?",
    "How does task deletion work?",
    "How are tasks searched?",
]


for query in queries:

    print("\n")
    print("=" * 80)
    print(f"QUERY: {query}")
    print("=" * 80)

    results = retriever.search(
        query,
        top_k=3,
    )

    for rank, result in enumerate(
        results,
        start=1,
    ):

        chunk = result["chunk"]

        print("\n" + "-" * 80)

        print(f"Rank: {rank}")
        print(
            f"Score: "
            f"{result['score']:.4f}"
        )

        print(
            f"File: {chunk['path']}"
        )

        print(
            f"Type: {chunk['chunk_type']}"
        )

        print(
            f"Name: {chunk['name']}"
        )

        print(
            f"Lines: "
            f"{chunk['start_line']}-"
            f"{chunk['end_line']}"
        )

        print("\nCode:")
        print(chunk["content"])


# --------------------------------------------------
# Metadata filtering test
# --------------------------------------------------

print("\n\n")
print("=" * 80)
print("METADATA FILTER TEST")
print("=" * 80)

results = retriever.search(
    "How are tasks created?",
    top_k=5,
    chunk_type="function",
)

print("\nOnly function chunks:\n")

for rank, result in enumerate(
    results,
    start=1,
):

    chunk = result["chunk"]

    print(
        f"{rank}. "
        f"{chunk['name']} "
        f"({chunk['path']}) "
        f"score={result['score']:.4f}"
    )
    # --------------------------------------------------
# MMR retrieval test
# --------------------------------------------------

print("\n\n")
print("=" * 80)
print("MMR RETRIEVAL TEST")
print("=" * 80)

results = retriever.mmr_search(
    "How are tasks created?",
    top_k=3,
    fetch_k=8,
    lambda_mult=0.7,
)

for rank, result in enumerate(
    results,
    start=1,
):

    chunk = result["chunk"]

    print(
        f"{rank}. "
        f"{chunk['name']} "
        f"({chunk['path']}) "
        f"score={result['score']:.4f}"
    )