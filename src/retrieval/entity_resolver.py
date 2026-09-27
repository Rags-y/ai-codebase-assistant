import json
import re
from pathlib import Path


CHUNKS_PATH = Path("data/processed/chunks.json")


class EntityResolver:

    def __init__(self):

        with CHUNKS_PATH.open(
            "r",
            encoding="utf-8",
        ) as f:
            self.chunks = json.load(f)

        self.entities = {}

        for chunk in self.chunks:

            name = chunk["name"]

            if name == "module_context":
                continue

            self.entities.setdefault(
                name.lower(),
                [],
            ).append(chunk)

    def _matches_entity(
        self,
        query: str,
        entity_name: str,
    ):

        query_lower = query.lower()

        # Exact entity match
        pattern = (
            r"(?<!\w)"
            + re.escape(entity_name)
            + r"(?!\w)"
        )

        if re.search(
            pattern,
            query_lower,
        ):
            return True

        # Simple singular/plural match
        if (
            entity_name.endswith("y")
            and entity_name[:-1] + "ies"
            in query_lower
        ):
            return True

        if (
            not entity_name.endswith("s")
            and entity_name + "s"
            in query_lower
        ):
            return True

        return False

    def resolve(
        self,
        query: str,
    ):

        matches = []

        for entity_name, chunks in self.entities.items():

            if not self._matches_entity(
                query,
                entity_name,
            ):
                continue

            for chunk in chunks:

                matches.append(
                    {
                        "entity": chunk["name"],
                        "chunk": chunk,
                        "match_length": len(
                            entity_name
                        ),
                    }
                )

        matches.sort(
            key=lambda result: result[
                "match_length"
            ],
            reverse=True,
        )

        return matches