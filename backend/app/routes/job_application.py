from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.job_application import JobApplication
from app.schemas.job_application import (
    JobApplicationCreate,
    JobApplicationResponse
)


router = APIRouter(
    prefix="/api/applications",
    tags=["Job Applications"]
)


# =========================================================
# GET ALL APPLICATIONS
# =========================================================

@router.get(
    "/",
    response_model=list[JobApplicationResponse]
)
def get_applications(
    db: Session = Depends(get_db)
):
    applications = (
        db.query(JobApplication)
        .order_by(JobApplication.created_at.desc())
        .all()
    )

    return applications


# =========================================================
# CREATE APPLICATION
# =========================================================

@router.post(
    "/",
    response_model=JobApplicationResponse
)
def create_application(
    application_data: JobApplicationCreate,
    db: Session = Depends(get_db)
):

    new_application = JobApplication(
        company=application_data.company,
        job_title=application_data.job_title,
        location=application_data.location,
        job_url=application_data.job_url,
        applied_date=application_data.applied_date,
        status=application_data.status,
        notes=application_data.notes
    )

    db.add(new_application)
    db.commit()
    db.refresh(new_application)

    return new_application


# =========================================================
# UPDATE APPLICATION STATUS
# =========================================================

@router.put("/{application_id}/status")
def update_application_status(
    application_id: int,
    status: str,
    db: Session = Depends(get_db)
):

    application = (
        db.query(JobApplication)
        .filter(JobApplication.id == application_id)
        .first()
    )

    if not application:
        raise HTTPException(
            status_code=404,
            detail="Application not found"
        )

    allowed_statuses = [
        "Applied",
        "Interview",
        "Selected",
        "Rejected"
    ]

    if status not in allowed_statuses:
        raise HTTPException(
            status_code=400,
            detail="Invalid status"
        )

    application.status = status

    db.commit()
    db.refresh(application)

    return application


# =========================================================
# DELETE ALL APPLICATIONS
# =========================================================

@router.delete("/")
def delete_all_applications(
    db: Session = Depends(get_db)
):

    applications = db.query(JobApplication).all()

    for application in applications:
        db.delete(application)

    db.commit()

    return {
        "success": True,
        "message": "All job applications deleted successfully"
    }


# =========================================================
# DELETE ONE APPLICATION
# =========================================================

@router.delete("/{application_id}")
def delete_application(
    application_id: int,
    db: Session = Depends(get_db)
):

    application = (
        db.query(JobApplication)
        .filter(JobApplication.id == application_id)
        .first()
    )

    if not application:
        raise HTTPException(
            status_code=404,
            detail="Application not found"
        )

    db.delete(application)
    db.commit()

    return {
        "success": True,
        "message": "Application deleted successfully"
    }