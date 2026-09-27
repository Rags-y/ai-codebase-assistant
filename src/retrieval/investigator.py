from src.retrieval.entity_resolver import (
    EntityResolver,
)

from src.graph.retriever import (
    GraphRetriever,
)


class CodeInvestigator:

    def __init__(self):

        self.entity_resolver = (
            EntityResolver()
        )

        self.graph_retriever = (
            GraphRetriever()
        )

    def detect_direction(
        self,
        query: str,
    ):

        query_lower = query.lower()

        reverse_keywords = [
            "which functions use",
            "what uses",
            "who uses",
            "what depends on",
            "which code uses",
            "which functions call",
            "who calls",
            "what calls",
        ]

        forward_keywords = [
            "what does",
            "what do",
            "what does this use",
            "what does this call",
            "what does it use",
            "what does it call",
            "what depends on",
        ]

        for keyword in reverse_keywords:

            if keyword in query_lower:

                return "reverse"

        for keyword in forward_keywords:

            if keyword in query_lower:

                return "forward"

        return "both"

    def investigate(
        self,
        query: str,
        max_hops: int = 1,
    ):

        # ------------------------------------------
        # Step 1: Resolve entities
        # ------------------------------------------

        entities = (
            self.entity_resolver.resolve(
                query
            )
        )

        if not entities:
            return []

        # ------------------------------------------
        # Step 2: Determine direction
        # ------------------------------------------

        direction = (
            self.detect_direction(query)
        )

        # ------------------------------------------
        # Step 3: Traverse graph
        # ------------------------------------------

        results = []

        seen = set()

        for entity in entities:

            chunk = entity["chunk"]

            chunk_id = chunk["chunk_id"]
            results.append(
    {
        "entity": entity["entity"],
        "direction": "entity",
        "hop": 0,
        "relationship": None,
        "chunk": chunk,
    }
)

            # --------------------------------------
            # Forward traversal
            # --------------------------------------

            if direction in (
                "forward",
                "both",
            ):

                related = (
                    self.graph_retriever.traverse(
                        chunk_id,
                        max_hops=max_hops,
                    )
                )

                for result in related:

                    related_chunk = (
                        result["chunk"]
                    )

                    related_id = (
                        related_chunk["chunk_id"]
                    )

                    if related_id in seen:
                        continue

                    seen.add(related_id)

                    results.append(
                        {
                            "entity": entity[
                                "entity"
                            ],
                            "direction": "forward",
                            "hop": result["hop"],
                            "relationship": (
                                result[
                                    "relationship"
                                ]
                            ),
                            "chunk": related_chunk,
                        }
                    )

            # --------------------------------------
            # Reverse traversal
            # --------------------------------------

            if direction in (
                "reverse",
                "both",
            ):

                related = (
                    self.graph_retriever.traverse_reverse(
                        chunk_id,
                        max_hops=max_hops,
                    )
                )

                for result in related:

                    related_chunk = (
                        result["chunk"]
                    )

                    related_id = (
                        related_chunk["chunk_id"]
                    )

                    if related_id in seen:
                        continue

                    seen.add(related_id)

                    results.append(
                        {
                            "entity": entity[
                                "entity"
                            ],
                            "direction": "reverse",
                            "hop": result["hop"],
                            "relationship": (
                                result[
                                    "relationship"
                                ]
                            ),
                            "chunk": related_chunk,
                        }
                    )

        return results