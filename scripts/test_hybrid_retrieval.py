from src.retrieval.semantic import SemanticRetriever
from src.graph.retriever import GraphRetriever


query = "How are tasks created and what validates the input?"


semantic_retriever = SemanticRetriever()
graph_retriever = GraphRetriever()


# --------------------------------------------------
# Step 1: Semantic retrieval
# --------------------------------------------------

semantic_results = semantic_retriever.search(
    query,
    top_k=3,
)


print("\n")
print("=" * 80)
print("SEMANTIC RETRIEVAL")
print("=" * 80)


for i, result in enumerate(
    semantic_results,
    start=1,
):

    chunk = result["chunk"]

    print(
        f"\n{i}. "
        f"{chunk['name']} "
        f"({chunk['path']}) "
        f"score={result['score']:.4f}"
    )


# --------------------------------------------------
# Step 2: Graph expansion
# --------------------------------------------------

graph_results = []


for result in semantic_results:

    chunk = result["chunk"]

    related = graph_retriever.get_related_chunks(
        chunk["chunk_id"]
    )

    graph_results.extend(related)


print("\n")
print("=" * 80)
print("GRAPH EXPANSION")
print("=" * 80)


for i, chunk in enumerate(
    graph_results,
    start=1,
):

    print(
        f"\n{i}. "
        f"{chunk['name']} "
        f"({chunk['path']})"
    )


# --------------------------------------------------
# Step 3: Combined context
# --------------------------------------------------

print("\n")
print("=" * 80)
print("COMBINED RETRIEVAL CONTEXT")
print("=" * 80)


seen = set()


for result in semantic_results:

    chunk = result["chunk"]

    if chunk["chunk_id"] in seen:
        continue

    seen.add(chunk["chunk_id"])

    print(
        f"\n--- {chunk['name']} "
        f"({chunk['path']}) ---"
    )

    print(chunk["content"])


for chunk in graph_results:

    if chunk["chunk_id"] in seen:
        continue

    seen.add(chunk["chunk_id"])

    print(
        f"\n--- {chunk['name']} "
        f"({chunk['path']}) [GRAPH] ---"
    )

    print(chunk["content"])