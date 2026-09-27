import json
from pathlib import Path

from groq import Groq

from src.retrieval.pipeline import RetrievalPipeline
from src.retrieval.context import ContextBuilder
from src.generation.generator import AnswerGenerator


QUESTIONS_PATH = Path(
    "data/processed/evaluation_questions.json"
)

REPORT_PATH = Path(
    "data/processed/relevance_evaluation.json"
)


class RelevanceEvaluator:

    def __init__(self):
        import os

        api_key = os.getenv("GROQ_API_KEY")

        if not api_key:
            raise ValueError(
                "GROQ_API_KEY environment variable is not set."
            )

        self.client = Groq(
            api_key=api_key
        )

        self.model = "openai/gpt-oss-120b"

    def evaluate(
        self,
        question,
        answer,
    ):
        prompt = f"""
You are evaluating the relevance of an AI codebase assistant's answer.

Determine whether the assistant directly answers the user's question.

Evaluation criteria:
- The answer should directly address what the user asked.
- The answer should contain the relevant code entities, behavior, or explanation.
- Extra useful detail is acceptable.
- Do not penalize concise answers.
- Do not judge whether the code itself is good or bad.
- Do not judge writing style.
- Do not evaluate factual grounding here.
- Focus ONLY on whether the answer addresses the question.
- Return ONLY valid JSON.

Required JSON format:
{{
  "relevant": true,
  "score": 1.0,
  "reason": "short explanation"
}}

Score guidelines:
- 1.0 = directly and completely answers the question
- 0.75 = mostly answers the question with a minor omission
- 0.5 = partially answers the question
- 0.25 = mostly fails to address the question
- 0.0 = does not answer the question

User question:
{question}

Assistant answer:
{answer}
"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            temperature=0,
        )

        content = response.choices[0].message.content

        try:
            return json.loads(content)
        except json.JSONDecodeError:
            return {
                "relevant": False,
                "score": 0.0,
                "reason": (
                    "Evaluator returned invalid JSON: "
                    + content
                ),
            }


def load_questions():
    with QUESTIONS_PATH.open(
        "r",
        encoding="utf-8",
    ) as f:
        return json.load(f)


def main():

    questions = load_questions()

    pipeline = RetrievalPipeline()
    context_builder = ContextBuilder()
    generator = AnswerGenerator()
    evaluator = RelevanceEvaluator()

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

        evaluation = evaluator.evaluate(
            query,
            answer,
        )

        result = {
            "id": question["id"],
            "question": query,
            "relevant": evaluation.get(
                "relevant",
                False,
            ),
            "score": evaluation.get(
                "score",
                0.0,
            ),
            "reason": evaluation.get(
                "reason",
                "",
            ),
            "answer": answer,
        }

        results.append(result)

        print(
            f"Relevance score: "
            f"{result['score']:.2f}"
        )

        print(
            f"Relevant: "
            f"{result['relevant']}"
        )

        print(
            f"Reason: "
            f"{result['reason']}"
        )

    average_score = (
        sum(
            result["score"]
            for result in results
        )
        / len(results)
    )

    relevant_count = sum(
        result["relevant"]
        for result in results
    )

    report = {
        "questions": len(results),
        "average_relevance": average_score,
        "relevant_questions": relevant_count,
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
    print("RELEVANCE EVALUATION")
    print("=" * 80)
    print(
        f"Questions: {len(results)}"
    )
    print(
        f"Average Relevance: "
        f"{average_score:.2f}"
    )
    print(
        f"Relevant Questions: "
        f"{relevant_count}/{len(results)}"
    )
    print(
        f"Report saved to: {REPORT_PATH}"
    )


if __name__ == "__main__":
    main()