from src.retrieval.semantic import SemanticRetriever
from src.retrieval.reranker import CodeReranker


query = "How are tasks created?"


retriever = SemanticRetriever()

results = retriever.search(
    query,
    top_k=8,
)


print()
print("=" * 80)
print("BEFORE RERANKING")
print("=" * 80)

for index, result in enumerate(
    results,
    start=1,
):
    chunk = result["chunk"]

    print(
        f"{index}. "
        f"{chunk['name']} "
        f"({chunk['path']}) "
        f"semantic={result['score']:.4f}"
    )


reranker = CodeReranker()

reranked = reranker.rerank(
    query,
    results,
    top_k=5,
)


print()
print("=" * 80)
print("AFTER RERANKING")
print("=" * 80)

for index, result in enumerate(
    reranked,
    start=1,
):
    chunk = result["chunk"]

    print(
        f"{index}. "
        f"{chunk['name']} "
        f"({chunk['path']}) "
        f"rerank={result['rerank_score']:.4f}"
    )