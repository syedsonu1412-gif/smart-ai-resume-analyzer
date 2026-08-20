from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class JobApplicationCreate(BaseModel):
    company: str
    job_title: str
    location: Optional[str] = None
    job_url: Optional[str] = None
    applied_date: Optional[datetime] = None
    status: str = "Applied"
    notes: Optional[str] = None


class JobApplicationResponse(BaseModel):
    id: int
    company: str
    job_title: str
    location: Optional[str]
    job_url: Optional[str]
    applied_date: Optional[datetime]
    status: str
    notes: Optional[str]

    class Config:
        from_attributes = True