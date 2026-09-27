from src.retrieval.entity_resolver import (
    EntityResolver,
)


resolver = EntityResolver()


queries = [
    "Which functions use the Task model?",
    "What does create_task use?",
    "How does update_task work?",
]


print("\n")
print("=" * 80)
print("ENTITY RESOLUTION")
print("=" * 80)


for query in queries:

    print(
        f"\nQuery: {query}"
    )

    results = resolver.resolve(
        query
    )

    if not results:

        print(
            "No entities found."
        )

        continue

    for result in results:

        chunk = result["chunk"]

        print(
            f"\nEntity: "
            f"{result['entity']}"
        )

        print(
            f"Chunk: "
            f"{chunk['name']}"
        )

        print(
            f"Path: "
            f"{chunk['path']}"
        )

        print(
            f"Type: "
            f"{chunk['chunk_type']}"
        )