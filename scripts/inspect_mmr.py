import numpy as np

from src.retrieval.semantic import SemanticRetriever


retriever = SemanticRetriever()

query = "How are tasks created?"

query_embedding = retriever.embedder.embed_query(
    query
)

similarities = (
    retriever.embeddings @ query_embedding
)

# Get the most relevant chunks first
candidate_indices = np.argsort(
    similarities
)[::-1][:8]

first_index = candidate_indices[0]

print("\n")
print("=" * 80)
print("MMR DIAGNOSTIC")
print("=" * 80)

first_chunk = retriever.chunks[first_index]

print("\nSelected first chunk:")
print(
    f"{first_chunk['name']} "
    f"({first_chunk['path']})"
)

print(
    f"Query relevance: "
    f"{similarities[first_index]:.4f}"
)

print("\nCandidate analysis:")
print("-" * 80)

lambda_mult = 0.7

for index in candidate_indices[1:]:

    relevance = similarities[index]

    redundancy = (
        retriever.embeddings[first_index]
        @ retriever.embeddings[index]
    )

    mmr_score = (
        lambda_mult * relevance
        - (1 - lambda_mult) * redundancy
    )

    chunk = retriever.chunks[index]

    print(
        f"{chunk['name']:<20} "
        f"relevance={relevance:.4f}  "
        f"redundancy={redundancy:.4f}  "
        f"MMR={mmr_score:.4f}"
    )