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


def main():

    with CHUNKS_PATH.open(
        "r",
        encoding="utf-8",
    ) as f:
        chunks = json.load(f)

    print(f"Loaded {len(chunks)} chunks")

    texts = [
        chunk["content"]
        for chunk in chunks
    ]

    embedder = CodeEmbedder()

    embeddings = embedder.embed_documents(
        texts
    )

    np.save(
        EMBEDDINGS_PATH,
        embeddings,
    )

    print(
        f"\nEmbedding shape: "
        f"{embeddings.shape}"
    )

    print(
        f"Saved embeddings to: "
        f"{EMBEDDINGS_PATH}"
    )


if __name__ == "__main__":
    main()