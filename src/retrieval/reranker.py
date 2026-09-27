from sentence_transformers import CrossEncoder


MODEL_NAME = "cross-encoder/ms-marco-MiniLM-L-6-v2"


class CodeReranker:

    def __init__(self):
        print(
            f"Loading reranker model: {MODEL_NAME}"
        )

        self.model = CrossEncoder(
            MODEL_NAME
        )

    def rerank(
        self,
        query: str,
        results: list[dict],
        top_k: int = 5,
    ):
        if not results:
            return []

        pairs = [
            (
                query,
                result["chunk"]["content"],
            )
            for result in results
        ]

        scores = self.model.predict(
            pairs
        )

        reranked = []

        for result, score in zip(
            results,
            scores,
        ):
            reranked.append(
                {
                    **result,
                    "rerank_score": float(score),
                }
            )

        reranked.sort(
            key=lambda result: result[
                "rerank_score"
            ],
            reverse=True,
        )

        return reranked[:top_k]