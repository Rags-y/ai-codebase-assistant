from src.retrieval.hybrid import HybridRetriever


retriever = HybridRetriever()


query = "Which functions use the Task model?"


results = retriever.search(
    query,
    top_k=3,
    graph_hops=1,
    direction="reverse",
    relationship="uses",
)


print("\n")
print("=" * 80)
print("RELATIONSHIP-AWARE RETRIEVAL")
print("=" * 80)


print(
    f"\nQuery: {query}"
)


for i, result in enumerate(
    results,
    start=1,
):

    chunk = result["chunk"]

    print(
        f"\n{i}. "
        f"{chunk['name']} "
        f"({chunk['path']})"
    )

    print(
        f"Source: {result['source']}"
    )

    if result["source"] == "semantic":

        print(
            f"Score: "
            f"{result['score']:.4f}"
        )

    else:

        print(
            f"Hop: "
            f"{result['hop']}"
        )

        print(
            f"Relationship: "
            f"{result['relationship']}"
        )

        print(
            f"Direction: "
            f"{result['direction']}"
        )

    print(
        f"Lines: "
        f"{chunk['start_line']}-"
        f"{chunk['end_line']}"
    )

    print("\nContent:")
    print(chunk["content"])