import re


# Skills that our system can recognize
SKILLS = [
    "Python",
    "Java",
    "JavaScript",
    "HTML",
    "CSS",
    "React",
    "Flask",
    "Django",
    "FastAPI",
    "SQL",
    "MySQL",
    "PostgreSQL",
    "MongoDB",
    "Git",
    "GitHub",
    "Docker",
    "AWS",
    "Azure",
    "Machine Learning",
    "Deep Learning",
    "NLP",
    "Pandas",
    "NumPy",
    "Scikit-learn",
    "TensorFlow",
    "Power BI",
    "Excel",
    "REST API",
]


def extract_job_skills(job_description: str) -> list:
    """
    Find technical skills mentioned in a job description.
    """

    found_skills = []

    text = job_description.lower()

    for skill in SKILLS:
        if skill.lower() in text:
            found_skills.append(skill)

    return found_skills


def calculate_match_score(
    resume_skills: list,
    job_skills: list
) -> int:
    """
    Calculate how well resume skills match job skills.
    """

    if not job_skills:
        return 0

    resume_set = {
        skill.lower()
        for skill in resume_skills
    }

    job_set = {
        skill.lower()
        for skill in job_skills
    }

    matching_skills = resume_set.intersection(job_set)

    score = (
        len(matching_skills)
        / len(job_set)
    ) * 100

    return round(score)


def find_missing_skills(
    resume_skills: list,
    job_skills: list
) -> list:
    """
    Find skills required by the job
    but missing from the resume.
    """

    resume_set = {
        skill.lower()
        for skill in resume_skills
    }

    missing = []

    for skill in job_skills:
        if skill.lower() not in resume_set:
            missing.append(skill)

    return missing