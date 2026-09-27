from src.ingestion.repository import scan_repository
from src.ingestion.code_chunker import chunk_python_file


REPOSITORY_PATH = (
    r"C:\Users\ragha\OneDrive\Documents\Projects"
    r"\fastapi-task-manager"
)


files = scan_repository(REPOSITORY_PATH)

for file in files:

    if file.language != "python":
        continue

    print("\n")
    print("#" * 80)
    print(f"FILE: {file.path}")
    print("#" * 80)

    chunks = chunk_python_file(file)

    print(f"\nFound {len(chunks)} code chunks\n")

    for chunk in chunks:

        print("-" * 80)

        print(f"Chunk ID: {chunk.chunk_id}")
        print(f"Type: {chunk.chunk_type}")
        print(f"Name: {chunk.name}")
        print(
            f"Lines: "
            f"{chunk.start_line}-{chunk.end_line}"
        )

        print("\nCode:")
        print(chunk.content)