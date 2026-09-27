import ast

from .chunks import CodeChunk
from .models import CodeFile


def chunk_python_file(code_file: CodeFile) -> list[CodeChunk]:

    tree = ast.parse(code_file.content)

    lines = code_file.content.splitlines()

    chunks = []

    # --------------------------------------------------
    # Module-level context
    # --------------------------------------------------

    context_nodes = []

    for node in tree.body:

        if isinstance(
            node,
            (
                ast.Import,
                ast.ImportFrom,
                ast.Assign,
                ast.AnnAssign,
                ast.AugAssign,
            ),
        ):
            context_nodes.append(node)

    if context_nodes:

        start_line = min(
            node.lineno
            for node in context_nodes
        )

        end_line = max(
            getattr(node, "end_lineno", node.lineno)
            for node in context_nodes
        )

        content = "\n".join(
            lines[start_line - 1:end_line]
        )

        chunks.append(
            CodeChunk(
                chunk_id=f"{code_file.file_id}:module-context",
                file_id=code_file.file_id,
                path=code_file.path,
                language=code_file.language,
                chunk_type="module_context",
                name="module_context",
                start_line=start_line,
                end_line=end_line,
                content=content,
                parent_file=code_file.file_id,
            )
        )

    # --------------------------------------------------
    # Functions and classes
    # --------------------------------------------------

    for node in ast.walk(tree):

        if not isinstance(
            node,
            (
                ast.FunctionDef,
                ast.AsyncFunctionDef,
                ast.ClassDef,
            ),
        ):
            continue

        start_line = node.lineno
        end_line = node.end_lineno

        content = "\n".join(
            lines[start_line - 1:end_line]
        )

        if isinstance(node, ast.ClassDef):
            chunk_type = "class"

        elif isinstance(node, ast.AsyncFunctionDef):
            chunk_type = "async_function"

        else:
            chunk_type = "function"

        chunk_id = (
            f"{code_file.file_id}:"
            f"{node.name}:"
            f"{start_line}-{end_line}"
        )

        chunks.append(
            CodeChunk(
                chunk_id=chunk_id,
                file_id=code_file.file_id,
                path=code_file.path,
                language=code_file.language,
                chunk_type=chunk_type,
                name=node.name,
                start_line=start_line,
                end_line=end_line,
                content=content,
                parent_file=code_file.file_id,
            )
        )

    return sorted(
        chunks,
        key=lambda chunk: chunk.start_line,
    )