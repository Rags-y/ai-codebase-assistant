import json
from pathlib import Path


RELATIONSHIPS_PATH = Path(
    "data/processed/relationships.json"
)

CHUNKS_PATH = Path(
    "data/processed/chunks.json"
)


class GraphRetriever:

    def __init__(self):

        with RELATIONSHIPS_PATH.open(
            "r",
            encoding="utf-8",
        ) as f:
            self.relationships = json.load(f)

        with CHUNKS_PATH.open(
            "r",
            encoding="utf-8",
        ) as f:
            self.chunks = json.load(f)

        self.chunk_map = {
            chunk["chunk_id"]: chunk
            for chunk in self.chunks
        }

    # ==================================================
    # Direct outgoing relationships
    # ==================================================

    def get_related_chunks(
        self,
        chunk_id: str,
        relationship: str | None = None,
    ):

        related_ids = []

        for relation in self.relationships:

            if relation["source_id"] != chunk_id:
                continue

            if (
                relationship is not None
                and relation["relationship"]
                != relationship
            ):
                continue

            related_ids.append(
                relation["target_id"]
            )

        return [
            self.chunk_map[related_id]
            for related_id in related_ids
            if related_id in self.chunk_map
        ]

    # ==================================================
    # Forward multi-hop traversal
    # ==================================================

    def traverse(
        self,
        chunk_id: str,
        max_hops: int = 2,
    ):

        visited = {chunk_id}
        frontier = [chunk_id]

        results = []

        for hop in range(max_hops):

            next_frontier = []

            for current_id in frontier:

                for relation in self.relationships:

                    if (
                        relation["source_id"]
                        != current_id
                    ):
                        continue

                    target_id = relation[
                        "target_id"
                    ]

                    if target_id in visited:
                        continue

                    if target_id not in self.chunk_map:
                        continue

                    visited.add(target_id)

                    next_frontier.append(
                        target_id
                    )

                    results.append(
                        {
                            "hop": hop + 1,
                            "relationship": relation[
                                "relationship"
                            ],
                            "direction": "outgoing",
                            "chunk": self.chunk_map[
                                target_id
                            ],
                        }
                    )

            frontier = next_frontier

            if not frontier:
                break

        return results

    # ==================================================
    # Reverse multi-hop traversal
    # ==================================================

    def traverse_reverse(
        self,
        chunk_id: str,
        max_hops: int = 2,
        relationship: str | None = None,
    ):

        visited = {chunk_id}
        frontier = [chunk_id]

        results = []

        for hop in range(max_hops):

            next_frontier = []

            for current_id in frontier:

                for relation in self.relationships:

                    if (
                        relation["target_id"]
                        != current_id
                    ):
                        continue

                    if (
                        relationship is not None
                        and relation["relationship"]
                        != relationship
                    ):
                        continue

                    source_id = relation[
                        "source_id"
                    ]

                    if source_id in visited:
                        continue

                    if source_id not in self.chunk_map:
                        continue

                    visited.add(source_id)

                    next_frontier.append(
                        source_id
                    )

                    results.append(
                        {
                            "hop": hop + 1,
                            "relationship": relation[
                                "relationship"
                            ],
                            "direction": "incoming",
                            "chunk": self.chunk_map[
                                source_id
                            ],
                        }
                    )

            frontier = next_frontier

            if not frontier:
                break

        return results