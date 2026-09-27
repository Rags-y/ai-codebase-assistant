from src.retrieval.semantic import SemanticRetriever
from src.retrieval.investigator import CodeInvestigator


class RetrievalPipeline:

    def __init__(self):

        self.semantic_retriever = (
            SemanticRetriever()
        )

        self.investigator = (
            CodeInvestigator()
        )

    def retrieve(
        self,
        query: str,
        semantic_top_k: int = 3,
        graph_hops: int = 1,
    ):

        semantic_results = (
            self.semantic_retriever.search(
                query,
                top_k=semantic_top_k,
            )
        )

        investigation_results = (
            self.investigator.investigate(
                query,
                max_hops=graph_hops,
            )
        )

        combined = []

        seen = set()

        # ------------------------------------------
        # Semantic results
        # ------------------------------------------

        for result in semantic_results:

            chunk = result["chunk"]

            chunk_id = chunk["chunk_id"]

            if chunk_id in seen:
                continue

            seen.add(chunk_id)

            combined.append(
                {
                    "chunk": chunk,
                    "source": "semantic",
                    "score": result["score"],
                    "hop": None,
                    "relationship": None,
                    "direction": None,
                }
            )

        # ------------------------------------------
        # Investigation results
        # ------------------------------------------

        for result in investigation_results:

            chunk = result["chunk"]

            chunk_id = chunk["chunk_id"]

            if chunk_id in seen:
                continue

            seen.add(chunk_id)

            is_entity = (
                result["direction"] == "entity"
            )

            combined.append(
                {
                    "chunk": chunk,
                    "source": (
                        "entity"
                        if is_entity
                        else "graph"
                    ),
                    "score": None,
                    "hop": result["hop"],
                    "relationship": (
                        result["relationship"]
                    ),
                    "direction": (
                        None
                        if is_entity
                        else result["direction"]
                    ),
                }
            )

        return combined