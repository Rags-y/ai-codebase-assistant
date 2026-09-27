import ast

from src.graph.models import CodeRelationship
from src.ingestion.chunks import CodeChunk


def extract_python_relationships(
    chunks: list[CodeChunk],
) -> list[CodeRelationship]:

    relationships = []

    # ------------------------------------------
    # Find class definitions
    # ------------------------------------------

    class_chunks = {
        chunk.name: chunk
        for chunk in chunks
        if chunk.chunk_type == "class"
    }

    # ------------------------------------------
    # Find function definitions
    # ------------------------------------------

    function_chunks = [
        chunk
        for chunk in chunks
        if chunk.chunk_type in (
            "function",
            "async_function",
        )
    ]

    function_map = {
        chunk.name: chunk
        for chunk in function_chunks
    }

    # ------------------------------------------
    # Class relationships
    # ------------------------------------------

    for class_chunk in class_chunks.values():

        tree = ast.parse(
            class_chunk.content
        )

        for node in ast.walk(tree):

            if not isinstance(node, ast.ClassDef):
                continue

            for base in node.bases:

                base_name = None

                if isinstance(base, ast.Name):
                    base_name = base.id

                elif isinstance(base, ast.Attribute):
                    base_name = base.attr

                if base_name not in class_chunks:
                    continue

                target_class = class_chunks[
                    base_name
                ]

                relationships.append(
                    CodeRelationship(
                        source_id=class_chunk.chunk_id,
                        target_id=target_class.chunk_id,
                        relationship="inherits",
                    )
                )

    # ------------------------------------------
    # Function relationships
    # ------------------------------------------

    for function_chunk in function_chunks:

        tree = ast.parse(
            function_chunk.content
        )

        # --------------------------------------
        # Class usage
        # --------------------------------------

        names_used = {
            node.id
            for node in ast.walk(tree)
            if isinstance(node, ast.Name)
        }

        for class_name, class_chunk in class_chunks.items():

            if class_name not in names_used:
                continue

            relationships.append(
                CodeRelationship(
                    source_id=function_chunk.chunk_id,
                    target_id=class_chunk.chunk_id,
                    relationship="uses",
                )
            )

        # --------------------------------------
        # Function calls
        # --------------------------------------

        for node in ast.walk(tree):

            if not isinstance(node, ast.Call):
                continue

            called_name = None

            if isinstance(node.func, ast.Name):
                called_name = node.func.id

            elif isinstance(node.func, ast.Attribute):
                called_name = node.func.attr

            if called_name not in function_map:
                continue

            target_function = function_map[
                called_name
            ]

            if (
                target_function.chunk_id
                == function_chunk.chunk_id
            ):
                continue

            relationships.append(
                CodeRelationship(
                    source_id=function_chunk.chunk_id,
                    target_id=target_function.chunk_id,
                    relationship="calls",
                )
            )

    return relationships