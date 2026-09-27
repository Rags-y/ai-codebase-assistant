from src.ingestion.repository import scan_repository


REPOSITORY_PATH = (
    r"C:\Users\ragha\OneDrive\Documents\Projects"
    r"\fastapi-task-manager"
)


files = scan_repository(REPOSITORY_PATH)

print(f"\nFound {len(files)} files\n")

for file in files:

    print("=" * 70)

    print(f"File ID: {file.file_id}")
    print(f"Path: {file.path}")
    print(f"Language: {file.language}")
    print(f"Type: {file.file_type}")
    print(f"Size: {file.size_bytes} bytes")
    print(f"Hash: {file.content_hash}")

    print("\nPreview:")
    print(file.content[:300])