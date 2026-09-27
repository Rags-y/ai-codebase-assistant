import json
from pathlib import Path

from src.ingestion.repository import scan_repository
from src.ingestion.code_chunker import chunk_python_file
from src.graph.extractor import (
    extract_python_relationships,
)


REPOSITORY_PATH = (
    r"C:\Users\ragha\OneDrive\Documents\Projects"
    r"\fastapi-task-manager"
)

OUTPUT_PATH = Path(
    "data/processed/relationships.json"
)


def build_graph():

    files = scan_repository(
        REPOSITORY_PATH
    )

    all_chunks = []

    for file in files:

        if file.language == "python":

            chunks = chunk_python_file(
                file
            )

            all_chunks.extend(chunks)

    relationships = (
        extract_python_relationships(
            all_chunks
        )
    )

    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with OUTPUT_PATH.open(
        "w",
        encoding="utf-8",
    ) as f:

        json.dump(
            [
                relationship.model_dump()
                for relationship in relationships
            ],
            f,
            indent=2,
        )

    print(
        f"Processed files: {len(files)}"
    )

    print(
        f"Generated chunks: "
        f"{len(all_chunks)}"
    )

    print(
        f"Generated relationships: "
        f"{len(relationships)}"
    )

    print(
        f"Saved to: {OUTPUT_PATH}"
    )


if __name__ == "__main__":
    build_graph()