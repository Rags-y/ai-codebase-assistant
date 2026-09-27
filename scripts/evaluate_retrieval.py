import json
from pathlib import Path

from src.retrieval.pipeline import RetrievalPipeline


QUESTIONS_PATH = Path("data/processed/evaluation_questions.json")
REPORT_PATH = Path("data/processed/retrieval_evaluation.json")


def load_questions():
    with QUESTIONS_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)


def evaluate_question(pipeline, question):
    query = question["question"]
    expected_chunks = set(question["expected_chunks"])

    results = pipeline.retrieve(
        query,
        semantic_top_k=3,
        graph_hops=1,
    )

    retrieved_names = [
        result["chunk"]["name"]
        for result in results
    ]

    retrieved_set = set(retrieved_names)

    matched = expected_chunks & retrieved_set

    recall = len(matched) / len(expected_chunks)

    precision = (
        len(matched) / len(retrieved_names)
        if retrieved_names
        else 0.0
    )

    return {
        "id": question["id"],
        "question": query,
        "expected": sorted(expected_chunks),
        "retrieved": retrieved_names,
        "matched": sorted(matched),
        "recall": recall,
        "precision": precision,
    }


def main():
    questions = load_questions()

    pipeline = RetrievalPipeline()

    results = []

    for question in questions:
        result = evaluate_question(
            pipeline,
            question,
        )

        results.append(result)

        print()
        print("=" * 80)
        print(result["id"])
        print(result["question"])
        print("-" * 80)
        print("Expected:", result["expected"])
        print("Retrieved:", result["retrieved"])
        print("Matched:", result["matched"])
        print(f"Recall: {result['recall']:.2f}")
        print(f"Precision: {result['precision']:.2f}")

    average_recall = (
        sum(result["recall"] for result in results)
        / len(results)
    )

    average_precision = (
        sum(result["precision"] for result in results)
        / len(results)
    )

    report = {
        "questions": len(results),
        "average_recall": average_recall,
        "average_precision": average_precision,
        "results": results,
    }

    REPORT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with REPORT_PATH.open("w", encoding="utf-8") as f:
        json.dump(
            report,
            f,
            indent=2,
        )

    print()
    print("=" * 80)
    print("RETRIEVAL EVALUATION")
    print("=" * 80)
    print(f"Questions: {len(results)}")
    print(f"Average Recall: {average_recall:.2f}")
    print(f"Average Precision: {average_precision:.2f}")
    print(f"Report saved to: {REPORT_PATH}")


if __name__ == "__main__":
    main()