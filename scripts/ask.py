from src.retrieval.pipeline import RetrievalPipeline
from src.retrieval.context import ContextBuilder
from src.generation.generator import AnswerGenerator


def main():
    print("=" * 70)
    print("AI CODEBASE & BUG INVESTIGATION ASSISTANT")
    print("=" * 70)

    query = input("\nAsk a question about the codebase: ").strip()

    if not query:
        print("Please enter a question.")
        return

    print("\n[1/3] Retrieving relevant code...")

    pipeline = RetrievalPipeline()

    results = pipeline.retrieve(
        query,
        semantic_top_k=5,
        graph_hops=1,
    )

    if not results:
        print("No relevant code was found.")
        return

    print(
        f"Found {len(results)} relevant code chunks."
    )

    print("\n[2/3] Building context...")

    context_builder = ContextBuilder()

    context = context_builder.build(
        results
    )

    print("[3/3] Generating answer...")

    generator = AnswerGenerator()

    answer = generator.generate(
        query=query,
        context=context,
    )

    print("\n" + "=" * 70)
    print("ANSWER")
    print("=" * 70)

    print(answer)

    print("\n" + "=" * 70)
    print("RETRIEVED CODE")
    print("=" * 70)

    for index, result in enumerate(
        results,
        start=1,
    ):
        chunk = result["chunk"]

        print(
            f"{index}. "
            f"{chunk['path']}:"
            f"{chunk['start_line']}-"
            f"{chunk['end_line']} "
            f"({chunk['name']})"
        )


if __name__ == "__main__":
    main()