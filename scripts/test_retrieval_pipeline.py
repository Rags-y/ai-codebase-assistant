from src.retrieval.pipeline import (
    RetrievalPipeline,
)


pipeline = RetrievalPipeline()


queries = [
    "Which functions use the Task model?",
    "What does create_task use?",
    "How are tasks created and what validates the input?",
]


print("\n")
print("=" * 80)
print("UNIFIED RETRIEVAL PIPELINE")
print("=" * 80)


for query in queries:

    print(
        f"\n\nQUERY: {query}"
    )

    results = pipeline.retrieve(
        query,
        semantic_top_k=3,
        graph_hops=1,
    )

    for i, result in enumerate(
        results,
        start=1,
    ):

        chunk = result["chunk"]

        print(
            f"\n{i}. "
            f"{chunk['name']} "
            f"({chunk['path']})"
        )

        print(
            f"Source: "
            f"{result['source']}"
        )

        if result["source"] == "semantic":

            print(
                f"Semantic score: "
                f"{result['score']:.4f}"
            )

        else:

            print(
                f"Graph hop: "
                f"{result['hop']}"
            )

            print(
                f"Relationship: "
                f"{result['relationship']}"
            )

            print(
                f"Direction: "
                f"{result['direction']}"
            )

        print(
            f"Lines: "
            f"{chunk['start_line']}-"
            f"{chunk['end_line']}"
        )

        print(
            "\nContent:"
        )

        print(
            chunk["content"]
        )