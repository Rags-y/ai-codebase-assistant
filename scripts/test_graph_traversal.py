from src.graph.retriever import GraphRetriever


retriever = GraphRetriever()


chunk_id = "routes.py:create_task:12-27"


results = retriever.traverse(
    chunk_id,
    max_hops=2,
)


print("\n")
print("=" * 80)
print("MULTI-HOP GRAPH TRAVERSAL")
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
        f"Chunk: "
        f"{chunk['name']} "
        f"({chunk['path']})"
    )

    print(
        f"Lines: "
        f"{chunk['start_line']}-"
        f"{chunk['end_line']}"
    )