from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
from pathlib import Path
import shutil
import json

from app.database import get_db
from app.models.resume import Resume

from app.services.resume_parser import (
    extract_text_from_pdf,
    find_skills,
    detect_domains,
    find_education,
    find_experience,
    calculate_resume_score,
    generate_recommendations
)


router = APIRouter(
    prefix="/api/resume",
    tags=["Resume"]
)


UPLOAD_FOLDER = Path("uploads/resumes")

UPLOAD_FOLDER.mkdir(
    parents=True,
    exist_ok=True
)


@router.post("/upload")
async def upload_resume(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):


    # Check PDF
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed"
        )

    # Save PDF
    file_path = UPLOAD_FOLDER / file.filename

    with file_path.open("wb") as buffer:
        shutil.copyfileobj(
            file.file,
            buffer
        )

    # Extract text
    extracted_text = extract_text_from_pdf(
        str(file_path)
    )

    # Find skills
    skills = find_skills(
        extracted_text
    )

    # Detect professional domains
    domains = detect_domains(
        extracted_text
    )

    # Find education
    education = find_education(
        extracted_text
    )

    # Find experience
    experience = find_experience(
        extracted_text
    )

    # Calculate resume score
    score = calculate_resume_score(
        extracted_text,
        skills,
        education,
        experience
    )

    # Generate recommendations
    recommendations = generate_recommendations(
        extracted_text,
        skills,
        education,
        experience
    )

    # Save analysis to database
    new_resume = Resume(
        filename=file.filename,
        file_path=str(file_path),
        extracted_text=extracted_text,
        score=score,
        detected_domains=json.dumps(domains),
        skills=json.dumps(skills),
        education=json.dumps(education),
        experience=json.dumps(experience),
        recommendations=json.dumps(recommendations)
    )

    db.add(new_resume)
    db.commit()
    db.refresh(new_resume)

    return {
        "success": True,
        "message": "Resume analyzed and saved successfully",
        "resume_id": new_resume.id,
        "filename": file.filename,
        "resume_score": score,
        "detected_domains": domains,
        "skills": skills,
        "education": education,
        "experience": experience,
        "recommendations": recommendations,
        "extracted_text": extracted_text
    }
@router.get("/latest")
def get_latest_resume(
    db: Session = Depends(get_db)
):
    resume = (
        db.query(Resume)
        .order_by(Resume.created_at.desc())
        .first()
    )

    if not resume:
        raise HTTPException(
            status_code=404,
            detail="No resume found"
        )

    return {
        "success": True,
        "resume_id": resume.id,
        "filename": resume.filename,
        "resume_score": resume.score,
        "detected_domains": json.loads(resume.detected_domains or "[]"),
        "skills": json.loads(resume.skills or "[]"),
        "education": json.loads(resume.education or "[]"),
        "experience": json.loads(resume.experience or "[]"),
        "recommendations": json.loads(resume.recommendations or "[]")
    }
@router.delete("/latest")
def delete_latest_resume(
    db: Session = Depends(get_db)
):
    resume = (
        db.query(Resume)
        .order_by(Resume.created_at.desc())
        .first()
    )

    if not resume:
        return {
            "success": True,
            "message": "No resume found"
        }

    file_path = Path(resume.file_path)

    if file_path.exists():
        file_path.unlink()

    db.delete(resume)
    db.commit()

    return {
        "success": True,
        "message": "Latest resume deleted successfully"
    }