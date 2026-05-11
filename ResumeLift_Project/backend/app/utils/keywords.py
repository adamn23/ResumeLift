from __future__ import annotations

import re
from collections import OrderedDict

DISPLAY_TERMS = {
    "react": "React",
    "next.js": "Next.js",
    "vue": "Vue",
    "angular": "Angular",
    "javascript": "JavaScript",
    "typescript": "TypeScript",
    "python": "Python",
    "java": "Java",
    "fastapi": "FastAPI",
    "flask": "Flask",
    "django": "Django",
    "postgresql": "PostgreSQL",
    "postgres": "PostgreSQL",
    "mysql": "MySQL",
    "sqlite": "SQLite",
    "mongodb": "MongoDB",
    "redis": "Redis",
    "docker": "Docker",
    "kubernetes": "Kubernetes",
    "aws": "AWS",
    "gcp": "GCP",
    "azure": "Azure",
    "git": "Git",
    "github": "GitHub",
    "rest": "REST",
    "api": "API",
    "sql": "SQL",
    "nosql": "NoSQL",
    "html": "HTML",
    "css": "CSS",
    "tailwind": "Tailwind",
    "tailwindcss": "TailwindCSS",
    "pytest": "pytest",
    "pandas": "Pandas",
    "numpy": "NumPy",
    "machine learning": "Machine Learning",
    "ml": "ML",
    "nlp": "NLP",
    "linux": "Linux",
    "ci/cd": "CI/CD",
    "ci cd": "CI/CD",
    "oauth": "OAuth",
    "jwt": "JWT",
    "graphql": "GraphQL",
    "microservices": "Microservices",
    "spark": "Spark",
    "airflow": "Airflow",
    "terraform": "Terraform",
    "slack": "Slack",
    "figma": "Figma",
    "agile": "Agile",
    "scrum": "Scrum",
    "leadership": "Leadership",
    "communication": "Communication",
    "testing": "Testing",
    "unit testing": "Unit Testing",
    "integration testing": "Integration Testing",
    "data analysis": "Data Analysis",
    "etl": "ETL",
    "backend": "Backend",
    "frontend": "Frontend",
    "full stack": "Full Stack",
}

TERM_PATTERNS = sorted(DISPLAY_TERMS.keys(), key=len, reverse=True)


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower()).strip()


def extract_keywords(text: str, max_keywords: int = 12) -> list[str]:
    if not text:
        return []

    normalized = normalize(text)
    found = OrderedDict()

    for term in TERM_PATTERNS:
        pattern = r"\b" + re.escape(term) + r"\b"
        if re.search(pattern, normalized):
            found[DISPLAY_TERMS[term]] = None

    if len(found) < max_keywords:
        words = re.findall(r"[a-zA-Z][a-zA-Z0-9+./#-]{2,}", text)
        for word in words:
            cleaned = word.strip(".,;:()[]{}")
            lowered = cleaned.lower()
            if lowered in {"resume", "project", "projects", "experience", "skills", "work", "team"}:
                continue
            if cleaned.istitle() and len(cleaned) > 2:
                found.setdefault(cleaned, None)
            if len(found) >= max_keywords:
                break

    return list(found.keys())[:max_keywords]


def compare_keywords(resume_text: str, job_text: str) -> tuple[list[str], list[str]]:
    resume_keywords = extract_keywords(resume_text, max_keywords=50)
    job_keywords = extract_keywords(job_text, max_keywords=50)

    resume_lower = {item.lower() for item in resume_keywords}
    matched = []
    missing = []

    for keyword in job_keywords:
        if keyword.lower() in resume_lower:
            matched.append(keyword)
        else:
            missing.append(keyword)

    return matched, missing
