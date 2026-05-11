from __future__ import annotations

from functools import lru_cache

import numpy as np
from sentence_transformers import SentenceTransformer

from app.core.config import get_settings

settings = get_settings()


@lru_cache(maxsize=1)
def get_model() -> SentenceTransformer:
    return SentenceTransformer(settings.sentence_transformer_model)


def embed_text(text: str) -> np.ndarray:
    model = get_model()
    vector = model.encode([text or ""], normalize_embeddings=True)
    return np.asarray(vector[0], dtype=np.float32)


def cosine_similarity_score(left: np.ndarray, right: np.ndarray) -> float:
    if left.size == 0 or right.size == 0:
        return 0.0
    return float(np.clip(np.dot(left, right), -1.0, 1.0))
