from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_settings
from app.models import JobDescription, MatchResult, Resume, User  # noqa: F401
from app.routes.auth import router as auth_router
from app.routes.dashboard import router as dashboard_router
from app.routes.jobs import router as jobs_router
from app.routes.matches import router as matches_router
from app.routes.resumes import router as resumes_router

settings = get_settings()

app = FastAPI(title="ResumeLift API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(resumes_router)
app.include_router(jobs_router)
app.include_router(matches_router)
app.include_router(dashboard_router)


@app.get("/health")
def health():
    return {"status": "ok"}
