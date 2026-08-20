import re
from pathlib import Path

from pypdf import PdfReader
from pypdf import PdfReader


# Broad skill database
SKILLS = {

    "Programming": [
        "Python",
        "Java",
        "JavaScript",
        "C",
        "C++",
        "C#",
        "PHP",
        "Ruby",
        "Go",
        "Kotlin",
        "Swift"
    ],

    "Web Development": [
        "HTML",
        "CSS",
        "React",
        "Angular",
        "Vue",
        "Django",
        "Flask",
        "FastAPI",
        "Spring Boot",
        "Node.js"
    ],

    "Data & Analytics": [
        "SQL",
        "MySQL",
        "PostgreSQL",
        "MongoDB",
        "Excel",
        "Power BI",
        "Tableau",
        "Pandas",
        "NumPy",
        "Statistics",
        "Data Analysis"
    ],

    "AI & Machine Learning": [
        "Machine Learning",
        "Deep Learning",
        "Artificial Intelligence",
        "NLP",
        "TensorFlow",
        "PyTorch",
        "Scikit-learn"
    ],

    "Cloud & DevOps": [
        "AWS",
        "Azure",
        "Google Cloud",
        "Docker",
        "Kubernetes",
        "Git",
        "GitHub",
        "Jenkins"
    ],

    "Business": [
        "Business Analysis",
        "Business Development",
        "Market Research",
        "Project Management",
        "CRM",
        "Sales",
        "Negotiation"
    ],

    "Human Resources": [
        "Recruitment",
        "Talent Acquisition",
        "Human Resources",
        "Employee Relations",
        "Payroll",
        "Onboarding",
        "Performance Management",
        "HRIS"
    ],

    "Marketing": [
        "Digital Marketing",
        "SEO",
        "SEM",
        "Social Media Marketing",
        "Content Marketing",
        "Google Analytics",
        "Email Marketing",
        "Brand Management"
    ],

    "Finance": [
        "Accounting",
        "Financial Analysis",
        "Financial Reporting",
        "Auditing",
        "Taxation",
        "Tally",
        "Bookkeeping",
        "Budgeting"
    ],

    "Healthcare": [
        "Healthcare",
        "Medical Coding",
        "Medical Billing",
        "Patient Care",
        "Clinical Research",
        "Hospital Management"
    ],

    "Design": [
        "UI/UX",
        "Figma",
        "Adobe Photoshop",
        "Adobe Illustrator",
        "Graphic Design",
        "Canva"
    ]
}


def extract_text_from_pdf(file_path: str) -> str:
    """
    Extract text from PDF resume.
    """

    reader = PdfReader(file_path)

    text = ""

    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text.strip()


def find_skills(text: str) -> list:
    """
    Find skills from all supported categories.
    """

    found_skills = []

    text_lower = text.lower()

    for category, skills in SKILLS.items():

        for skill in skills:

            if skill.lower() in text_lower:

                if skill not in found_skills:
                    found_skills.append(skill)

    return found_skills


def detect_domains(text: str) -> list:
    """
    Identify the likely professional domains
    based on skills found in the resume.
    """

    text_lower = text.lower()

    detected_domains = []

    for category, skills in SKILLS.items():

        matches = 0

        for skill in skills:

            if skill.lower() in text_lower:
                matches += 1

        if matches >= 2:
            detected_domains.append(category)

    return detected_domains


def find_education(text: str) -> list:
    """
    Detect common education information.
    """

    education_keywords = [
        "B.Tech",
        "B.E",
        "Bachelor",
        "Bachelors",
        "M.Tech",
        "M.E",
        "Master",
        "MCA",
        "MBA",
        "BCA",
        "B.Sc",
        "M.Sc",
        "PhD",
        "Diploma",
        "Computer Science",
        "Information Technology",
        "Business Administration",
        "Commerce",
        "Engineering",
        "Arts"
    ]

    found_education = []

    text_lower = text.lower()

    for education in education_keywords:

        if education.lower() in text_lower:

            if education not in found_education:
                found_education.append(education)

    return found_education


def find_experience(text: str) -> list:
    """
    Detect experience-related information.
    """

    experience_keywords = [
        "experience",
        "work experience",
        "internship",
        "intern",
        "employment",
        "worked",
        "professional experience",
        "career"
    ]

    found_experience = []

    text_lower = text.lower()

    for keyword in experience_keywords:

        if keyword.lower() in text_lower:

            found_experience.append(keyword)

    return found_experience


def find_resume_sections(text: str) -> list:
    """
    Detect important resume sections.
    """

    sections = [
        "profile",
        "summary",
        "objective",
        "education",
        "experience",
        "skills",
        "projects",
        "certifications",
        "certificates",
        "achievements",
        "languages",
        "interests"
    ]

    found_sections = []

    text_lower = text.lower()

    for section in sections:

        if section in text_lower:
            found_sections.append(section)

    return found_sections


def calculate_resume_score(
    text: str,
    skills: list,
    education: list,
    experience: list
) -> int:
    """
    Calculate a general resume quality score.

    This score does NOT depend on Python specifically.
    """

    score = 0

    # --------------------------------
    # 1. Resume content
    # --------------------------------

    if len(text) >= 1500:
        score += 20

    elif len(text) >= 800:
        score += 15

    elif len(text) >= 400:
        score += 10

    else:
        score += 5


    # --------------------------------
    # 2. Skills
    # --------------------------------

    if len(skills) >= 10:
        score += 20

    elif len(skills) >= 6:
        score += 15

    elif len(skills) >= 3:
        score += 10

    elif len(skills) >= 1:
        score += 5


    # --------------------------------
    # 3. Education
    # --------------------------------

    if len(education) >= 2:
        score += 15

    elif len(education) == 1:
        score += 10


    # --------------------------------
    # 4. Experience
    # --------------------------------

    if experience:
        score += 15


    # --------------------------------
    # 5. Resume sections
    # --------------------------------

    sections = find_resume_sections(text)

    important_sections = [
        "summary",
        "profile",
        "education",
        "experience",
        "skills",
        "projects",
        "certifications"
    ]

    section_score = 0

    for section in important_sections:

        if section in sections:
            section_score += 3

    score += min(section_score, 20)


    return min(score, 100)


def generate_recommendations(
    text: str,
    skills: list,
    education: list,
    experience: list
) -> list:
    """
    Generate general resume improvement suggestions.
    """

    recommendations = []

    sections = find_resume_sections(text)

    if "summary" not in sections and "profile" not in sections:

        recommendations.append(
            "Add a professional summary or profile section."
        )

    if "skills" not in sections:

        recommendations.append(
            "Add a clearly organized skills section."
        )

    if "experience" not in sections:

        recommendations.append(
            "Add relevant work experience or internships."
        )

    if "projects" not in sections:

        recommendations.append(
            "Add projects that demonstrate your practical skills."
        )

    if "certifications" not in sections and "certificates" not in sections:

        recommendations.append(
            "Add relevant certifications or courses."
        )

    if len(skills) < 5:

        recommendations.append(
            "Add more relevant skills related to your target role."
        )

    if len(text) < 500:

        recommendations.append(
            "Add more detailed information about your experience, projects and achievements."
        )

    if not recommendations:

        recommendations.append(
            "Resume has good overall structure. Consider adding measurable achievements."
        )

    return recommendations

