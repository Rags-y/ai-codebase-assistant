import ast

from src.ingestion.repository import scan_repository


REPOSITORY_PATH = (
    r"C:\Users\ragha\OneDrive\Documents\Projects"
    r"\fastapi-task-manager"
)


files = scan_repository(REPOSITORY_PATH)

for file in files:

    if file.language != "python":
        continue

    print("\n" + "=" * 80)
    print(f"FILE: {file.path}")
    print("=" * 80)

    tree = ast.parse(file.content)

    for node in tree.body:

        print(
            f"{type(node).__name__}"
            f" | line={getattr(node, 'lineno', '-')}"
        )

        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            print(f"  name: {node.name}")

        elif isinstance(node, ast.ClassDef):
            print(f"  name: {node.name}")

        elif isinstance(node, (ast.Import, ast.ImportFrom)):
            print("  import statement")

        elif isinstance(node, ast.Assign):
            print("  assignment")