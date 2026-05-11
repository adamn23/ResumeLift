from __future__ import annotations

from app.services.embedding_service import cosine_similarity_score, embed_text
from app.utils.keywords import compare_keywords


def analyze_match(resume_text: str, job_text: str) -> dict:
    matched_keywords, missing_keywords = compare_keywords(resume_text, job_text)

    resume_vec = embed_text(resume_text)
    job_vec = embed_text(job_text)
    embedding_similarity = max(0.0, cosine_similarity_score(resume_vec, job_vec))

    keyword_pool = len(matched_keywords) + len(missing_keywords)
    keyword_coverage = (len(matched_keywords) / keyword_pool) if keyword_pool else 0.0

    score = (embedding_similarity * 0.75) + (keyword_coverage * 0.25)
    match_score = round(max(0.0, min(1.0, score)) * 100, 2)

    return {
        "match_score": match_score,
        "matched_keywords": matched_keywords,
        "missing_keywords": missing_keywords,
    }
