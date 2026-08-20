from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine

from app.models.user import User
from app.models.resume import Resume
from app.models.job_application import JobApplication


from app.routes.auth import router as auth_router
from app.routes.resume import router as resume_router
from app.routes.job import router as job_router
from app.routes.job_application import router as job_application_router


# Create database tables
Base.metadata.create_all(bind=engine)


# Create FastAPI application
app = FastAPI(
    title="Smart AI Resume Analyzer & Job Tracker",
    description="AI-powered resume analysis and job tracking system",
    version="1.0.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Register routes
app.include_router(auth_router)
app.include_router(resume_router)
app.include_router(job_router)

app.include_router(job_application_router)


@app.get("/")
def home():
    return {
        "success": True,
        "message": "Smart AI Resume Analyzer API is running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


@app.get("/api/project")
def project_info():
    return {
        "project": "Smart AI Resume Analyzer & Job Tracker",
        "version": "1.0.0",
        "technology": {
            "backend": "Python FastAPI",
            "frontend": "React",
            "database": "MySQL",
            "ai": "AI/NLP"
        },
        "features": [
            "Resume Analysis",
            "ATS Score",
            "Job Matching",
            "Skill Gap Analysis",
            "Job Application Tracking"
        ]
    }