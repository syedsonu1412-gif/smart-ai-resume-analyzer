from fastapi import APIRouter

from app.schemas.job import JobMatchRequest

from app.services.job_matcher import (
    extract_job_skills,
    calculate_match_score,
    find_missing_skills
)


router = APIRouter(
    prefix="/api/job",
    tags=["Job Matching"]
)


@router.post("/match")
def match_resume_with_job(
    data: JobMatchRequest
):

    # Get skills from job description
    job_skills = extract_job_skills(
        data.job_description
    )

    # Get skills from resume
    resume_skills = extract_job_skills(
        data.resume_text
    )

    # Calculate matching percentage
    match_score = calculate_match_score(
        resume_skills,
        job_skills
    )

    # Find missing skills
    missing_skills = find_missing_skills(
        resume_skills,
        job_skills
    )

    # Find matching skills
    matching_skills = [
        skill
        for skill in job_skills
        if skill.lower()
        in [s.lower() for s in resume_skills]
    ]

    return {
        "success": True,
        "match_score": match_score,
        "resume_skills": resume_skills,
        "job_required_skills": job_skills,
        "matching_skills": matching_skills,
        "missing_skills": missing_skills
    }