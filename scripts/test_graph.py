from src.ingestion.repository import scan_repository
from src.ingestion.code_chunker import chunk_python_file
from src.graph.extractor import (
    extract_python_relationships,
)


REPOSITORY_PATH = (
    r"C:\Users\ragha\OneDrive\Documents\Projects"
    r"\fastapi-task-manager"
)


files = scan_repository(
    REPOSITORY_PATH
)

all_chunks = []

for file in files:

    if file.language == "python":

        chunks = chunk_python_file(file)

        all_chunks.extend(chunks)


relationships = (
    extract_python_relationships(
        all_chunks
    )
)


print("\n")
print("=" * 80)
print("CODE RELATIONSHIPS")
print("=" * 80)


for relationship in relationships:

    source = next(
        chunk
        for chunk in all_chunks
        if chunk.chunk_id
        == relationship.source_id
    )

    target = next(
        chunk
        for chunk in all_chunks
        if chunk.chunk_id
        == relationship.target_id
    )

    print(
        f"\n{source.name}"
        f" ({source.path})"
    )

    print(
        f"    --{relationship.relationship}-->"
    )

    print(
        f"    {target.name}"
        f" ({target.path})"
    )