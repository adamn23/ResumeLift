# ResumeLift

ResumeLift is a clean, beginner-friendly full-stack AI resume analyzer.

## What it does

- User registration and login with JWT
- PDF resume upload and text extraction
- Job description saving
- Resume-to-job matching with sentence embeddings
- Cosine similarity scoring
- Keyword overlap and missing keyword detection
- AI-generated resume feedback with the OpenAI API
- PostgreSQL storage with SQLAlchemy and Alembic
- Dockerized frontend, backend, and database

## Tech stack

Frontend: React, Vite, TailwindCSS, Axios, React Router  
Backend: FastAPI, PostgreSQL, SQLAlchemy, JWT, Alembic  
AI: sentence-transformers, cosine similarity, OpenAI API  
Infrastructure: Docker, Docker Compose

## Project structure

```text
backend/
  app/
    core/
    database/
    models/
    routes/
    schemas/
    services/
    utils/
  alembic/
  Dockerfile
  requirements.txt

frontend/
  src/
    components/
    context/
    pages/
    services/
  Dockerfile
  nginx.conf
```

## Setup with Docker

1. Copy the example env files:
   ```bash
   cp backend/.env.example backend/.env
   cp frontend/.env.example frontend/.env
   ```

2. Edit `backend/.env` and add your `OPENAI_API_KEY` if you want AI feedback from OpenAI.

3. Start everything:
   ```bash
   docker compose up --build
   ```

4. Open:
   - Frontend: `http://localhost:3000`
   - Backend: `http://localhost:8000/docs`

## Local backend setup

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
alembic upgrade head
uvicorn app.main:app --reload
```

## Local frontend setup

```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

## API routes

Auth:
- `POST /register`
- `POST /login`

Resumes:
- `POST /resumes/upload-resume`
- `GET /resumes`

Job descriptions:
- `POST /job-description`
- `GET /job-description`

Matching:
- `POST /analyze-match`
- `POST /generate-feedback`
- `GET /matches`

Dashboard:
- `GET /dashboard`

## Example request payloads

### Register
```json
{
  "email": "student@example.com",
  "password": "password123"
}
```

### Save job description
```json
{
  "title": "Junior Full Stack Developer",
  "description": "We are looking for a developer with React, FastAPI, PostgreSQL, Docker, and AWS experience."
}
```

### Analyze match
```json
{
  "resume_id": 1,
  "job_description_id": 1
}
```

### Example match response
```json
{
  "match_score": 84,
  "missing_keywords": ["Docker", "AWS"],
  "matched_keywords": ["React", "FastAPI", "PostgreSQL"]
}
```

### Example feedback response
```json
{
  "feedback": [
    "Add more measurable impact metrics",
    "Include Docker experience",
    "Improve project bullet clarity"
  ]
}
```
