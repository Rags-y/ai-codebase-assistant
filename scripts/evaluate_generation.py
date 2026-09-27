import json
from pathlib import Path

from src.retrieval.pipeline import RetrievalPipeline
from src.retrieval.context import ContextBuilder
from src.generation.generator import AnswerGenerator


QUESTIONS_PATH = Path(
    "data/processed/evaluation_questions.json"
)

REPORT_PATH = Path(
    "data/processed/generation_evaluation.json"
)


def load_questions():
    with QUESTIONS_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)


def evaluate_answer(answer, expected_concepts):
    answer_lower = answer.lower()

    matched = [
        concept
        for concept in expected_concepts
        if concept.lower() in answer_lower
    ]

    score = (
        len(matched) / len(expected_concepts)
        if expected_concepts
        else 0.0
    )

    return matched, score


def main():
    questions = load_questions()

    pipeline = RetrievalPipeline()
    context_builder = ContextBuilder()
    generator = AnswerGenerator()

    results = []

    for question in questions:

        query = question["question"]

        print()
        print("=" * 80)
        print(question["id"])
        print(query)
        print("-" * 80)

        retrieval_results = pipeline.retrieve(
            query,
            semantic_top_k=3,
            graph_hops=1,
        )

        context = context_builder.build(
            retrieval_results
        )

        answer = generator.generate(
            query,
            context,
        )

        matched, score = evaluate_answer(
            answer,
            question["expected_concepts"],
        )

        result = {
            "id": question["id"],
            "question": query,
            "expected_concepts": question[
                "expected_concepts"
            ],
            "matched_concepts": matched,
            "concept_score": score,
            "answer": answer,
        }

        results.append(result)

        print("Matched concepts:")
        print(matched)

        print(
            f"Concept score: {score:.2f}"
        )

        print()
        print("Answer:")
        print(answer)

    average_score = (
        sum(
            result["concept_score"]
            for result in results
        )
        / len(results)
    )

    report = {
        "questions": len(results),
        "average_concept_score": average_score,
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
    print("GENERATION EVALUATION")
    print("=" * 80)
    print(
        f"Questions: {len(results)}"
    )
    print(
        f"Average Concept Score: "
        f"{average_score:.2f}"
    )
    print(
        f"Report saved to: {REPORT_PATH}"
    )


if __name__ == "__main__":
    main()