from src.graph.retriever import GraphRetriever


retriever = GraphRetriever()


chunk_id = "models.py:Task:4-11"


results = retriever.traverse_reverse(
    chunk_id,
    max_hops=1,
    relationship="uses",
)


print("\n")
print("=" * 80)
print("REVERSE GRAPH TRAVERSAL")
print("=" * 80)


print(
    f"\nStarting chunk: {chunk_id}"
)


for result in results:

    chunk = result["chunk"]

    print(
        f"\nHop {result['hop']}"
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
        f"Chunk: "
        f"{chunk['name']} "
        f"({chunk['path']})"
    )

    print(
        f"Lines: "
        f"{chunk['start_line']}-"
        f"{chunk['end_line']}"
    )