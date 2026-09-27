from src.retrieval.semantic import SemanticRetriever
from src.graph.retriever import GraphRetriever


class HybridRetriever:

    def __init__(self):

        self.semantic_retriever = (
            SemanticRetriever()
        )

        self.graph_retriever = (
            GraphRetriever()
        )

    def search(
        self,
        query: str,
        top_k: int = 3,
        graph_hops: int = 1,
        direction: str = "both",
        relationship: str | None = None,
    ):

        # ------------------------------------------
        # Step 1: Semantic retrieval
        # ------------------------------------------

        semantic_results = (
            self.semantic_retriever.search(
                query,
                top_k=top_k,
            )
        )

        # ------------------------------------------
        # Step 2: Graph expansion
        # ------------------------------------------

        graph_results = []

        seen_graph_chunks = set()

        for result in semantic_results:

            chunk = result["chunk"]

            # --------------------------------------
            # Forward graph traversal
            # --------------------------------------

            if direction in (
                "forward",
                "both",
            ):

                related_chunks = (
                    self.graph_retriever.traverse(
                        chunk["chunk_id"],
                        max_hops=graph_hops,
                    )
                )

                for related in related_chunks:

                    if (
                        relationship is not None
                        and related["relationship"]
                        != relationship
                    ):
                        continue

                    related_chunk = (
                        related["chunk"]
                    )

                    chunk_id = (
                        related_chunk["chunk_id"]
                    )

                    if chunk_id in seen_graph_chunks:
                        continue

                    seen_graph_chunks.add(
                        chunk_id
                    )

                    graph_results.append(
                        {
                            "chunk": related_chunk,
                            "hop": related["hop"],
                            "relationship": (
                                related[
                                    "relationship"
                                ]
                            ),
                            "direction": "outgoing",
                        }
                    )

            # --------------------------------------
            # Reverse graph traversal
            # --------------------------------------

            if direction in (
                "reverse",
                "both",
            ):

                related_chunks = (
                    self.graph_retriever.traverse_reverse(
                        chunk["chunk_id"],
                        max_hops=graph_hops,
                    )
                )

                for related in related_chunks:

                    if (
                        relationship is not None
                        and related["relationship"]
                        != relationship
                    ):
                        continue

                    related_chunk = (
                        related["chunk"]
                    )

                    chunk_id = (
                        related_chunk["chunk_id"]
                    )

                    if chunk_id in seen_graph_chunks:
                        continue

                    seen_graph_chunks.add(
                        chunk_id
                    )

                    graph_results.append(
                        {
                            "chunk": related_chunk,
                            "hop": related["hop"],
                            "relationship": (
                                related[
                                    "relationship"
                                ]
                            ),
                            "direction": "incoming",
                        }
                    )

        # ------------------------------------------
        # Step 3: Combine results
        # ------------------------------------------

        combined = []

        seen = set()

        # Semantic results first
        for result in semantic_results:

            chunk = result["chunk"]

            chunk_id = chunk["chunk_id"]

            if chunk_id in seen:
                continue

            seen.add(chunk_id)

            combined.append(
                {
                    "source": "semantic",
                    "score": result["score"],
                    "chunk": chunk,
                }
            )

        # Graph results second
        for result in graph_results:

            chunk = result["chunk"]

            chunk_id = chunk["chunk_id"]

            if chunk_id in seen:
                continue

            seen.add(chunk_id)

            combined.append(
                {
                    "source": "graph",
                    "score": None,
                    "chunk": chunk,
                    "hop": result["hop"],
                    "relationship": (
                        result["relationship"]
                    ),
                    "direction": (
                        result["direction"]
                    ),
                }
            )

        return combined