from src.graph.retriever import GraphRetriever


retriever = GraphRetriever()


chunk_id = "routes.py:create_task:12-27"


results = retriever.get_related_chunks(
    chunk_id
)


print("\n")
print("=" * 80)
print("GRAPH RETRIEVAL")
print("=" * 80)


print(
    f"\nStarting chunk: {chunk_id}"
)


for result in results:

    print(
        f"\nRelated chunk:"
    )

    print(
        f"  Name: {result['name']}"
    )

    print(
        f"  Path: {result['path']}"
    )

    print(
        f"  Type: {result['chunk_type']}"
    )

    print(
        f"  Lines: "
        f"{result['start_line']}-"
        f"{result['end_line']}"
    )

    print(
        f"\n{result['content']}"
    )