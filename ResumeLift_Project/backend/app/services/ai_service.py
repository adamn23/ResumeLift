from __future__ import annotations

import json
import re
from typing import Any

from openai import OpenAI

from app.core.config import get_settings

settings = get_settings()


def _fallback_feedback(missing_keywords: list[str], matched_keywords: list[str]) -> list[str]:
    feedback = [
        "Add more measurable impact metrics to your bullet points.",
        "Make sure your strongest projects are described with action verbs and clear outcomes.",
    ]
    if missing_keywords:
        feedback.append(f"Add missing keywords where they are truthful and relevant: {', '.join(missing_keywords[:5])}.")
    if "Docker" in missing_keywords:
        feedback.append("Mention Docker if you have used it in projects, deployment, or local development.")
    if "AWS" in missing_keywords:
        feedback.append("Highlight any cloud experience, especially AWS, if it appears in your background.")
    if matched_keywords:
        feedback.append(f"Keep emphasizing strengths already present: {', '.join(matched_keywords[:5])}.")
    return feedback[:5]


def _extract_json_array(text: str) -> list[str] | None:
    try:
        data = json.loads(text)
        if isinstance(data, dict) and "feedback" in data and isinstance(data["feedback"], list):
            return [str(item) for item in data["feedback"]]
        if isinstance(data, list):
            return [str(item) for item in data]
    except Exception:
        pass

    match = re.search(r"\[(.*)\]", text, re.DOTALL)
    if match:
        try:
            arr = json.loads(f"[{match.group(1)}]")
            if isinstance(arr, list):
                return [str(item) for item in arr]
        except Exception:
            pass
    return None


def generate_feedback(
    resume_text: str,
    job_text: str,
    missing_keywords: list[str] | None = None,
    matched_keywords: list[str] | None = None,
) -> list[str]:
    missing_keywords = missing_keywords or []
    matched_keywords = matched_keywords or []

    if not settings.openai_api_key:
        return _fallback_feedback(missing_keywords, matched_keywords)

    client = OpenAI(api_key=settings.openai_api_key)
    prompt = f"""You are ResumeLift, an ATS-friendly resume coach.

Return only valid JSON in this format:
{{"feedback": ["item 1", "item 2", "item 3"]}}

Rules:
- Give 3 to 5 concise suggestions.
- Focus on measurable impact, ATS optimization, and stronger bullet wording.
- Do not invent experience.
- Keep the wording practical and beginner-friendly.

Resume:
{resume_text[:6000]}

Job description:
{job_text[:6000]}

Missing keywords:
{missing_keywords}

Matched keywords:
{matched_keywords}
"""

    response = client.responses.create(
        model=settings.openai_model,
        input=prompt,
    )
    text = getattr(response, "output_text", "") or ""
    parsed = _extract_json_array(text)
    if parsed:
        return parsed[:5]
    return _fallback_feedback(missing_keywords, matched_keywords)
