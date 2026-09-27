import json
from pathlib import Path

import numpy as np

from src.embeddings.embedder import CodeEmbedder


CHUNKS_PATH = Path(
    "data/processed/chunks.json"
)

EMBEDDINGS_PATH = Path(
    "data/processed/embeddings.npy"
)


class SemanticRetriever:

    def __init__(self):

        with CHUNKS_PATH.open(
            "r",
            encoding="utf-8",
        ) as f:
            self.chunks = json.load(f)

        self.embeddings = np.load(
            EMBEDDINGS_PATH
        )

        self.embedder = CodeEmbedder()

        print(
            f"Loaded {len(self.chunks)} chunks"
        )

        print(
            f"Embedding matrix: "
            f"{self.embeddings.shape}"
        )

    # ==================================================
    # Standard semantic search
    # ==================================================

    def search(
        self,
        query: str,
        top_k: int = 5,
        chunk_type: str | None = None,
        language: str | None = None,
        path: str | None = None,
    ):

        query_embedding = (
            self.embedder.embed_query(query)
        )

        similarities = (
            self.embeddings @ query_embedding
        )

        candidate_indices = np.arange(
            len(self.chunks)
        )

        # ------------------------------------------
        # Metadata filtering
        # ------------------------------------------

        if chunk_type is not None:

            candidate_indices = [
                index
                for index in candidate_indices
                if self.chunks[index]["chunk_type"]
                == chunk_type
            ]

        if language is not None:

            candidate_indices = [
                index
                for index in candidate_indices
                if self.chunks[index]["language"]
                == language
            ]

        if path is not None:

            candidate_indices = [
                index
                for index in candidate_indices
                if self.chunks[index]["path"]
                == path
            ]

        # ------------------------------------------
        # Rank candidates
        # ------------------------------------------

        ranked_indices = sorted(
            candidate_indices,
            key=lambda index: similarities[index],
            reverse=True,
        )

        # ------------------------------------------
        # Build results
        # ------------------------------------------

        results = []

        for index in ranked_indices[:top_k]:

            results.append(
                {
                    "score": float(
                        similarities[index]
                    ),
                    "chunk": self.chunks[index],
                }
            )

        return results

    # ==================================================
    # MMR search
    # ==================================================

    def mmr_search(
        self,
        query: str,
        top_k: int = 5,
        fetch_k: int = 10,
        lambda_mult: float = 0.7,
        chunk_type: str | None = None,
        language: str | None = None,
        path: str | None = None,
    ):

        query_embedding = (
            self.embedder.embed_query(query)
        )

        similarities = (
            self.embeddings @ query_embedding
        )

        candidate_indices = np.arange(
            len(self.chunks)
        )

        # ------------------------------------------
        # Metadata filtering
        # ------------------------------------------

        if chunk_type is not None:

            candidate_indices = [
                index
                for index in candidate_indices
                if self.chunks[index]["chunk_type"]
                == chunk_type
            ]

        if language is not None:

            candidate_indices = [
                index
                for index in candidate_indices
                if self.chunks[index]["language"]
                == language
            ]

        if path is not None:

            candidate_indices = [
                index
                for index in candidate_indices
                if self.chunks[index]["path"]
                == path
            ]

        # ------------------------------------------
        # Candidate pool
        # ------------------------------------------

        candidate_indices = sorted(
            candidate_indices,
            key=lambda index: similarities[index],
            reverse=True,
        )[:fetch_k]

        selected_indices = []

        # ------------------------------------------
        # MMR selection
        # ------------------------------------------

        while (
            candidate_indices
            and len(selected_indices) < top_k
        ):

            if not selected_indices:

                best_index = candidate_indices[0]

            else:

                best_index = None
                best_score = -float("inf")

                for candidate in candidate_indices:

                    relevance = similarities[
                        candidate
                    ]

                    selected_embeddings = (
                        self.embeddings[
                            selected_indices
                        ]
                    )

                    candidate_embedding = (
                        self.embeddings[
                            candidate
                        ]
                    )

                    redundancy = np.max(
                        selected_embeddings
                        @ candidate_embedding
                    )

                    mmr_score = (
                        lambda_mult * relevance
                        - (1 - lambda_mult)
                        * redundancy
                    )

                    if mmr_score > best_score:

                        best_score = mmr_score
                        best_index = candidate

            candidate_indices.remove(
                best_index
            )

            selected_indices.append(
                best_index
            )

        # ------------------------------------------
        # Build results
        # ------------------------------------------

        results = []

        for index in selected_indices:

            results.append(
                {
                    "score": float(
                        similarities[index]
                    ),
                    "chunk": self.chunks[index],
                }
            )

        return results