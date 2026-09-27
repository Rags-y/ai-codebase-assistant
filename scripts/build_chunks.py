import json
from pathlib import Path

from src.ingestion.repository import scan_repository
from src.ingestion.code_chunker import chunk_python_file


REPOSITORY_PATH = (
    r"C:\Users\ragha\OneDrive\Documents\Projects"
    r"\fastapi-task-manager"
)

OUTPUT_PATH = Path("data/processed/chunks.json")


def build_chunks():

    files = scan_repository(REPOSITORY_PATH)

    all_chunks = []

    for file in files:

        if file.language == "python":
            chunks = chunk_python_file(file)
        else:
            # We will handle JavaScript and other languages later.
            continue

        all_chunks.extend(chunks)

    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with OUTPUT_PATH.open(
        "w",
        encoding="utf-8",
    ) as f:

        json.dump(
            [chunk.model_dump() for chunk in all_chunks],
            f,
            indent=2,
            ensure_ascii=False,
        )

    print(f"Processed files: {len(files)}")
    print(f"Generated chunks: {len(all_chunks)}")
    print(f"Saved to: {OUTPUT_PATH}")


if __name__ == "__main__":
    build_chunks()