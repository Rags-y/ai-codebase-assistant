import json
from pathlib import Path

from src.retrieval.semantic import SemanticRetriever
from src.retrieval.reranker import CodeReranker


QUESTIONS_PATH = Path(
    "data/processed/evaluation_questions.json"
)

REPORT_PATH = Path(
    "data/processed/reranking_evaluation.json"
)


def load_questions():
    with QUESTIONS_PATH.open(
        "r",
        encoding="utf-8",
    ) as f:
        return json.load(f)


def evaluate_question(
    retriever,
    reranker,
    question,
):
    query = question["question"]

    expected_chunks = set(
        question["expected_chunks"]
    )

    # Retrieve a larger candidate pool first.
    candidates = retriever.search(
        query,
        top_k=8,
    )

    # Rerank candidates and keep the final top 5.
    results = reranker.rerank(
        query,
        candidates,
        top_k=5,
    )

    retrieved_names = [
        result["chunk"]["name"]
        for result in results
    ]

    retrieved_set = set(
        retrieved_names
    )

    matched = (
        expected_chunks
        & retrieved_set
    )

    recall = (
        len(matched)
        / len(expected_chunks)
    )

    precision = (
        len(matched)
        / len(retrieved_names)
        if retrieved_names
        else 0.0
    )

    return {
        "id": question["id"],
        "question": query,
        "expected": sorted(
            expected_chunks
        ),
        "retrieved": retrieved_names,
        "matched": sorted(matched),
        "recall": recall,
        "precision": precision,
    }


def main():

    questions = load_questions()

    retriever = SemanticRetriever()
    reranker = CodeReranker()

    results = []

    for question in questions:

        result = evaluate_question(
            retriever,
            reranker,
            question,
        )

        results.append(result)

        print()
        print("=" * 80)
        print(result["id"])
        print(result["question"])
        print("-" * 80)
        print(
            "Expected:",
            result["expected"],
        )
        print(
            "Retrieved:",
            result["retrieved"],
        )
        print(
            "Matched:",
            result["matched"],
        )
        print(
            f"Recall: "
            f"{result['recall']:.2f}"
        )
        print(
            f"Precision: "
            f"{result['precision']:.2f}"
        )

    average_recall = (
        sum(
            result["recall"]
            for result in results
        )
        / len(results)
    )

    average_precision = (
        sum(
            result["precision"]
            for result in results
        )
        / len(results)
    )

    report = {
        "questions": len(results),
        "retrieval": {
            "candidate_top_k": 8,
            "final_top_k": 5,
        },
        "average_recall": average_recall,
        "average_precision": average_precision,
        "results": results,
    }

    REPORT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with REPORT_PATH.open(
        "w",
        encoding="utf-8",
    ) as f:
        json.dump(
            report,
            f,
            indent=2,
        )

    print()
    print("=" * 80)
    print("RERANKING EVALUATION")
    print("=" * 80)
    print(
        f"Questions: {len(results)}"
    )
    print(
        f"Average Recall: "
        f"{average_recall:.2f}"
    )
    print(
        f"Average Precision: "
        f"{average_precision:.2f}"
    )
    print(
        f"Report saved to: {REPORT_PATH}"
    )


if __name__ == "__main__":
    main()