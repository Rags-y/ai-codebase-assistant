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
    "data/processed/faithfulness_evaluation.json"
)


class FaithfulnessEvaluator:

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
        context,
        answer,
    ):
        prompt = f"""
You are evaluating the faithfulness of an AI codebase assistant.

The assistant must answer using ONLY the provided code context.

Determine whether the answer is supported by the context.

Rules:
- Do not judge whether the code itself is good or bad.
- Do not judge writing quality.
- Check only whether the claims in the answer are supported by the provided context.
- If a claim is directly supported by the code context, count it as supported.
- If a claim is contradicted by the context, count it as unsupported.
- If the answer contains a minor wording difference but the meaning is clearly supported, count it as supported.
- Do not penalize concise explanations.
- Return ONLY valid JSON.

Required JSON format:
{{
  "faithful": true,
  "score": 1.0,
  "supported_claims": [
    "claim 1"
  ],
  "unsupported_claims": [
    "claim 2"
  ],
  "reason": "short explanation"
}}

Score guidelines:
- 1.0 = all important claims are supported
- 0.75 = mostly supported, with a minor unsupported claim
- 0.5 = several important claims are unsupported
- 0.25 = mostly unsupported
- 0.0 = answer is not grounded in the context

Question:
{question}

Code context:
{context}

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
                "faithful": False,
                "score": 0.0,
                "supported_claims": [],
                "unsupported_claims": [
                    "Evaluator returned invalid JSON."
                ],
                "reason": content,
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
    evaluator = FaithfulnessEvaluator()

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
            context,
            answer,
        )

        result = {
            "id": question["id"],
            "question": query,
            "faithful": evaluation.get(
                "faithful",
                False,
            ),
            "score": evaluation.get(
                "score",
                0.0,
            ),
            "supported_claims": evaluation.get(
                "supported_claims",
                [],
            ),
            "unsupported_claims": evaluation.get(
                "unsupported_claims",
                [],
            ),
            "reason": evaluation.get(
                "reason",
                "",
            ),
            "answer": answer,
        }

        results.append(result)

        print(
            f"Faithfulness score: "
            f"{result['score']:.2f}"
        )

        print(
            f"Faithful: "
            f"{result['faithful']}"
        )

        if result["unsupported_claims"]:
            print("Unsupported claims:")
            for claim in result[
                "unsupported_claims"
            ]:
                print(f"- {claim}")

    average_score = (
        sum(
            result["score"]
            for result in results
        )
        / len(results)
    )

    faithful_count = sum(
        result["faithful"]
        for result in results
    )

    report = {
        "questions": len(results),
        "average_faithfulness": average_score,
        "faithful_questions": faithful_count,
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
    print("FAITHFULNESS EVALUATION")
    print("=" * 80)
    print(
        f"Questions: {len(results)}"
    )
    print(
        f"Average Faithfulness: "
        f"{average_score:.2f}"
    )
    print(
        f"Fully Faithful Questions: "
        f"{faithful_count}/{len(results)}"
    )
    print(
        f"Report saved to: {REPORT_PATH}"
    )


if __name__ == "__main__":
    main()