from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="AI Resume Analyzer")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ResumeInput(BaseModel):
    resume_text: str
    target_role: str
    job_description: str = ""

ROLE_SKILLS = {
    "sde": {
        "Data Structures": ["data structures", "dsa", "ds"],
        "Algorithms": ["algorithms", "algorithm", "algo"],
        "Python": ["python"],
        "Java": ["java"],
        "C++": ["c++", "cpp"],
        "OOPS": ["oops", "oop", "object oriented", "object-oriented"],
        "Git": ["git", "github", "version control"],
        "SQL": ["sql", "mysql", "postgres", "database"],
        "API": ["api", "rest api", "fastapi", "flask", "django"],
    },
    "data analyst": {
        "Python": ["python"],
        "SQL": ["sql", "mysql", "postgres"],
        "Excel": ["excel", "spreadsheet"],
        "Power BI": ["power bi", "powerbi"],
        "Statistics": ["statistics", "stats"],
        "Data Visualization": ["visualization", "dashboard", "charts"],
    },
    "frontend developer": {
        "HTML": ["html"],
        "CSS": ["css"],
        "JavaScript": ["javascript", "js"],
        "React": ["react", "reactjs"],
        "Git": ["git", "github"],
        "Responsive Design": ["responsive", "mobile friendly"],
    },
    "backend developer": {
        "Python": ["python"],
        "Java": ["java"],
        "FastAPI": ["fastapi"],
        "Flask": ["flask"],
        "SQL": ["sql", "database", "mysql", "postgres"],
        "API": ["api", "rest"],
        "Git": ["git", "github"],
    },
    "ml engineer": {
        "Python": ["python"],
        "Machine Learning": ["machine learning", "ml"],
        "Pandas": ["pandas"],
        "NumPy": ["numpy"],
        "Scikit-learn": ["scikit", "sklearn", "scikit-learn"],
        "Deep Learning": ["deep learning", "tensorflow", "pytorch"],
    },
}
def detect_sections(resume):
    sections = {
        "Education": ["education", "degree", "b.e", "b.tech", "college", "university"],
        "Skills": ["skills", "technical skills", "technologies"],
        "Projects": ["projects", "project"],
        "Experience": ["experience", "internship", "intern"],
        "Certifications": ["certification", "certified", "course"],
        "Achievements": ["achievement", "award", "rank", "hackathon"],
        "Links": ["github", "linkedin", "portfolio"],
    }

    found = []
    missing = []

    for section, keywords in sections.items():
        if any(keyword in resume for keyword in keywords):
            found.append(section)
        else:
            missing.append(section)

    return found, missing


def analyze_job_description_match(resume, job_description):
    if not job_description.strip():
        return {
            "jd_match_percent": 0,
            "jd_matched_keywords": [],
            "jd_missing_keywords": [],
        }

    important_words = [
        "python", "java", "c++", "sql", "react", "fastapi", "flask",
        "django", "machine learning", "excel", "power bi", "git",
        "api", "html", "css", "javascript", "data structures",
        "algorithms", "communication", "problem solving"
    ]

    jd = job_description.lower()

    jd_keywords = [word for word in important_words if word in jd]
    matched = [word for word in jd_keywords if word in resume]
    missing = [word for word in jd_keywords if word not in resume]

    match_percent = round((len(matched) / len(jd_keywords)) * 100) if jd_keywords else 0

    return {
        "jd_match_percent": match_percent,
        "jd_matched_keywords": matched,
        "jd_missing_keywords": missing,
    }


def find_weak_bullets(resume_text):
    weak_phrases = [
        "worked on",
        "helped in",
        "responsible for",
        "participated in",
        "made a",
        "created a website",
        "did project",
    ]

    lines = resume_text.split("\n")
    weak_lines = []

    for line in lines:
        clean_line = line.strip()
        if any(phrase in clean_line.lower() for phrase in weak_phrases):
            weak_lines.append(clean_line)

    return weak_lines[:5]


def rewrite_bullets(weak_bullets):
    rewritten = []

    for bullet in weak_bullets:
        rewritten.append({
            "original": bullet,
            "improved": f"Improved version: {bullet} with clear technology, measurable impact, and outcome."
        })

    return rewritten


def generate_interview_questions(resume, target_role, missing_skills):
    questions = [
        "Tell me about yourself.",
        f"Why are you interested in the {target_role} role?",
        "Explain your best project and your exact contribution.",
        "What challenges did you face in your project and how did you solve them?",
    ]

    if "project" in resume:
        questions.append("Which technologies did you use in your project and why?")

    for skill in missing_skills[:3]:
        questions.append(f"You have not strongly shown {skill}. How would you rate yourself in it?")

    return questions


def generate_learning_roadmap(missing_skills):
    roadmap = []

    for index, skill in enumerate(missing_skills[:5], start=1):
        roadmap.append({
            "day": index,
            "skill": skill,
            "task": f"Learn basics of {skill}, build one small example, and add it to a resume project."
        })

    return roadmap


def check_resume_quality(resume):
    checks = []

    if not any(char.isdigit() for char in resume):
        checks.append("Add measurable numbers like percentages, user counts, marks, ranks, or performance improvements.")

    if "github" not in resume:
        checks.append("Add your GitHub profile link.")

    if "linkedin" not in resume:
        checks.append("Add your LinkedIn profile link.")

    if len(resume.split()) < 150:
        checks.append("Resume content looks too short. Add more details about projects, skills, and achievements.")

    weak_words = ["hardworking", "good communication", "team player"]
    if any(word in resume for word in weak_words):
        checks.append("Replace generic soft-skill claims with proof through achievements or project outcomes.")

    return checks


def recommend_roles(resume):
    role_scores = {}

    for role, skills in ROLE_SKILLS.items():
        score = 0
        for variations in skills.values():
            if any(variation in resume for variation in variations):
                score += 1
        role_scores[role] = score

    sorted_roles = sorted(role_scores.items(), key=lambda item: item[1], reverse=True)
    return [role for role, score in sorted_roles[:3] if score > 0]
def detect_sections(resume):
    sections = {
        "Education": ["education", "degree", "b.e", "b.tech", "college", "university"],
        "Skills": ["skills", "technical skills", "technologies"],
        "Projects": ["projects", "project"],
        "Experience": ["experience", "internship", "intern", "work experience"],
        "Certifications": ["certification", "certified", "course"],
        "Achievements": ["achievement", "award", "rank", "hackathon"],
        "Links": ["github", "linkedin", "portfolio"],
    }

    found_sections = []
    missing_sections = []

    for section, keywords in sections.items():
        if any(keyword in resume for keyword in keywords):
            found_sections.append(section)
        else:
            missing_sections.append(section)

    return found_sections, missing_sections


def recommend_roles(resume):
    role_scores = {}

    for role, skills in ROLE_SKILLS.items():
        score = 0

        for variations in skills.values():
            if any(variation in resume for variation in variations):
                score += 1

        role_scores[role] = score

    sorted_roles = sorted(role_scores.items(), key=lambda item: item[1], reverse=True)

    return [
        {"role": role, "match_count": score}
        for role, score in sorted_roles[:3]
        if score > 0
    ]


def generate_action_checklist(missing_skills, missing_sections, issues):
    checklist = []

    for skill in missing_skills[:3]:
        checklist.append(f"Add or improve evidence for {skill} through projects or coursework.")

    for section in missing_sections[:3]:
        checklist.append(f"Add a clear {section} section to your resume.")

    for issue in issues[:3]:
        checklist.append(issue)

    if not checklist:
        checklist.append("Resume looks strong. Add more measurable impact to make it stand out.")

    return checklist[:7]

@app.get("/")
def root():
    return {
        "status": "Backend running",
        "available_roles": list(ROLE_SKILLS.keys())
    }

@app.post("/analyze-text")
def analyze_resume(data: ResumeInput):
    resume = data.resume_text.lower().strip()
    job_description = data.job_description.lower()
    role = data.target_role.lower().strip()
    

    if not resume:
        raise HTTPException(status_code=400, detail="Resume text cannot be empty.")

    if role not in ROLE_SKILLS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported role. Choose from: {', '.join(ROLE_SKILLS.keys())}"
        )

    skills = ROLE_SKILLS[role]
    matched = []
    missing = []
    issues = []

    for skill, variations in skills.items():
        if any(variation in resume for variation in variations):
            matched.append(skill)
        else:
            missing.append(skill)

    skill_match_percent = round((len(matched) / len(skills)) * 100)

    structure_score = 0

    if "project" in resume or "projects" in resume:
        structure_score += 15
    else:
        issues.append("Projects section is missing or not clearly highlighted.")

    if any(word in resume for word in ["intern", "internship", "experience"]):
        structure_score += 15
    else:
        issues.append("No internship or work experience mentioned.")

    if any(word in resume for word in ["achievement", "award", "rank", "certification"]):
        structure_score += 10
    else:
        issues.append("Achievements or certifications are missing.")

    if any(char.isdigit() for char in resume):
        structure_score += 10
    else:
        issues.append("Add measurable impact using numbers, percentages, or counts.")

    skill_score = skill_match_percent * 0.6
    ats_score = min(100, round(skill_score + structure_score))

    if ats_score >= 80:
        verdict = "Strong"
    elif ats_score >= 60:
        verdict = "Good, but needs improvement"
    else:
        verdict = "Needs significant improvement"

    if missing:
        ai_feedback = (
            f"For the {data.target_role} role, your resume is missing important skills: "
            f"{', '.join(missing)}. Add relevant projects, tools, and measurable outcomes."
        )
    else:
        ai_feedback = (
            f"Your resume aligns well with the {data.target_role} role. "
            "Improve it further by adding stronger metrics and project impact."
        )
    found_sections, missing_sections = detect_sections(resume)
    jd_analysis = analyze_job_description_match(resume, job_description)
    weak_bullets = find_weak_bullets(data.resume_text)
    rewritten_bullets = rewrite_bullets(weak_bullets)
    interview_questions = generate_interview_questions(resume, data.target_role, missing)
    learning_roadmap = generate_learning_roadmap(missing)
    quality_checks = check_resume_quality(resume)
    recommended_roles = recommend_roles(resume) 
    return {
        "target_role": role,
        "ats_score": ats_score,
        "verdict": verdict,
        "skill_match_percent": skill_match_percent,
        "matched_skills": matched,
        "missing_skills": missing,
        "issues": issues,
        "ai_feedback": ai_feedback,
        "found_sections": found_sections,
        "missing_sections": missing_sections,
        "jd_match_percent": jd_analysis["jd_match_percent"],
        "jd_matched_keywords": jd_analysis["jd_matched_keywords"],
        "jd_missing_keywords": jd_analysis["jd_missing_keywords"],
        "weak_bullets": weak_bullets,
        "rewritten_bullets": rewritten_bullets,
        "interview_questions": interview_questions,
        "learning_roadmap": learning_roadmap,
        "quality_checks": quality_checks,
        "recommended_roles": recommended_roles,
    }