from pathlib import Path
from datetime import datetime
import hashlib

from .models import CodeFile


SUPPORTED_EXTENSIONS = {
    ".py": "python",
    ".js": "javascript",
    ".ts": "typescript",
    ".tsx": "typescript",
    ".jsx": "javascript",
    ".java": "java",
    ".go": "go",
    ".rs": "rust",
    ".cpp": "cpp",
    ".c": "c",
    ".md": "markdown",
}


IGNORED_DIRECTORIES = {
    ".git",
    ".venv",
    "venv",
    "node_modules",
    "__pycache__",
    ".pytest_cache",
}


def calculate_hash(content: str) -> str:
    return hashlib.sha256(
        content.encode("utf-8")
    ).hexdigest()


def scan_repository(repository_path: str) -> list[CodeFile]:

    root = Path(repository_path)

    code_files = []

    for path in root.rglob("*"):

        if not path.is_file():
            continue

        if any(
            ignored in path.parts
            for ignored in IGNORED_DIRECTORIES
        ):
            continue

        language = SUPPORTED_EXTENSIONS.get(path.suffix.lower())

        if language is None:
            continue

        try:
            content = path.read_text(
                encoding="utf-8"
            )
        except UnicodeDecodeError:
            continue

        relative_path = path.relative_to(root)

        code_file = CodeFile(
            file_id=str(relative_path),
            path=str(relative_path),
            filename=path.name,
            language=language,
            file_type="source_code"
            if language != "markdown"
            else "documentation",
            content=content,
            size_bytes=path.stat().st_size,
            modified_at=datetime.fromtimestamp(
                path.stat().st_mtime
            ),
            content_hash=calculate_hash(content),
        )

        code_files.append(code_file)

    return code_files