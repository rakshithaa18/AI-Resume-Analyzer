import io
import tempfile

import docx2txt
import pdfplumber
import requests
import streamlit as st
from fpdf import FPDF

st.set_page_config(page_title="AI Resume Analyzer", layout="wide")

BACKEND_URL = "http://127.0.0.1:8000"

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
}

h1, h2, h3, h4, h5, h6, p, label, span {
    color: #f8fafc !important;
}

[data-testid="stFileUploader"] section {
    background-color: #1f3a44 !important;
    color: #f8fafc !important;
    border-radius: 14px;
}

[data-testid="stFileUploader"] * {
    color: #f8fafc !important;
}

textarea, input {
    background-color: #0f172a !important;
    color: #f8fafc !important;
    caret-color: #f8fafc !important;
    border-radius: 12px !important;
}

textarea::placeholder,
input::placeholder {
    color: #94a3b8 !important;
}

.stButton > button {
    background: linear-gradient(135deg, #22c55e, #16a34a);
    color: white !important;
    font-weight: 600;
    border-radius: 12px;
    border: none;
    padding: 0.65rem 1.2rem;
}

[data-testid="stMetricValue"] {
    color: #22c55e !important;
}

[data-testid="stAlert"] {
    background-color: rgba(239, 68, 68, 0.25) !important;
    color: #f8fafc !important;
}

.glass {
    background: rgba(255,255,255,0.12);
    padding: 25px;
    border-radius: 18px;
    margin-bottom: 25px;
    box-shadow: 0 12px 30px rgba(0,0,0,0.3);
}
</style>
""", unsafe_allow_html=True)


def extract_text(file):
    if not file:
        return ""

    ext = file.name.split(".")[-1].lower()

    if ext == "pdf":
        text = ""
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                text += (page.extract_text() or "") + "\n"
        return text

    if ext == "docx":
        with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as temp:
            temp.write(file.read())
            temp_path = temp.name
        return docx2txt.process(temp_path)

    if ext == "txt":
        return file.read().decode("utf-8", errors="ignore")

    return ""


def create_pdf_report(response):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "AI Resume Analysis Report", ln=True)

    pdf.set_font("Arial", size=12)
    pdf.ln(6)

    report = f"""
Target Role: {response.get("target_role", "N/A")}
ATS Score: {response.get("ats_score", 0)}%
Skill Match: {response.get("skill_match_percent", 0)}%

Matched Skills:
{", ".join(response.get("matched_skills", [])) or "None"}

Missing Skills:
{", ".join(response.get("missing_skills", [])) or "None"}

Improvements Needed:
{chr(10).join(response.get("issues", [])) or "No major issues found."}

AI Feedback:
{response.get("ai_feedback", "No feedback available.")}
"""

    pdf.multi_cell(0, 8, report)

    pdf_bytes = pdf.output(dest="S").encode("latin-1")
    return io.BytesIO(pdf_bytes)


st.markdown("<h1 style='text-align:center;'>AI Resume Analyzer</h1>", unsafe_allow_html=True)
st.markdown(
    "<p style='text-align:center;'>ATS Score | Skill Match | AI Feedback | PDF Report</p>",
    unsafe_allow_html=True
)

uploaded = st.file_uploader("Upload Resume", type=["pdf", "docx", "txt"])
resume_text = st.text_area("Or paste resume text", height=220)
job_description = st.text_area("Paste Job Description", height=180)
role = st.selectbox("Target Role", ["sde", "data analyst","frontend developer", "backend developer", "ml engineer"])

if st.button("Analyze Resume"):
    text = extract_text(uploaded) if uploaded else resume_text

    if not text.strip():
        st.error("Please upload or paste resume text.")
        st.stop()

    try:
        response = requests.post(
            f"{BACKEND_URL}/analyze-text",
            json={
                "resume_text": text,
                "target_role": role,
                "job_description": job_description
            },            timeout=20
        )

        if response.status_code != 200:
            st.error(response.json().get("detail", "Backend returned an error."))
            st.stop()

        result = response.json()

    except requests.exceptions.ConnectionError:
        st.error("Backend is not running. Start FastAPI first using: uvicorn backend:app --reload")
        st.stop()
    except requests.exceptions.RequestException as error:
        st.error(f"Request failed: {error}")
        st.stop()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("ATS Score", f"{result.get('ats_score', 0)}%")
        st.progress(result.get("ats_score", 0) / 100)

    with col2:
        st.metric("Skill Match", f"{result.get('skill_match_percent', 0)}%")
        st.progress(result.get("skill_match_percent", 0) / 100)

    with col3:
        st.metric("Verdict", result.get("verdict", "N/A"))

    st.subheader("Matched Skills")
    st.success(", ".join(result.get("matched_skills", [])) or "No matched skills found.")

    st.subheader("Missing Skills")
    st.error(", ".join(result.get("missing_skills", [])) or "No missing skills found.")

    st.subheader("Job Description Match")
    st.metric("JD Match", f"{result.get('jd_match_percent', 0)}%")
    st.progress(result.get("jd_match_percent", 0) / 100)

    st.write("Matched JD Keywords:")
    st.success(", ".join(result.get("jd_matched_keywords", [])) or "No JD keywords matched.")

    st.write("Missing JD Keywords:")
    st.error(", ".join(result.get("jd_missing_keywords", [])) or "No missing JD keywords.")
    st.subheader("AI Feedback")
    st.info(result.get("ai_feedback", "No feedback available."))
    
    st.subheader("Resume Section Check")

    st.write("Detected Sections:")
    st.success(", ".join(result.get("found_sections", [])) or "No sections detected.")

    st.write("Missing Sections:")
    st.warning(", ".join(result.get("missing_sections", [])) or "No major sections missing.")

    st.subheader("Resume Bullet Rewriter")

    rewritten_bullets = result.get("rewritten_bullets", [])

    if rewritten_bullets:
        for item in rewritten_bullets:
            st.write("Original:")
            st.warning(item.get("original"))
            st.write("Improved:")
            st.success(item.get("improved"))
    else:
        st.success("No weak bullets detected.")



    st.subheader("Improvements Needed")
    issues = result.get("issues", [])

    if issues:
        for issue in issues:
            st.warning(issue)
    else:
        st.success("No major structural issues found.")
    st.subheader("Personalized Learning Roadmap")

    roadmap = result.get("learning_roadmap", [])

    if roadmap:
        for item in roadmap:
            st.write(f"Day {item.get('day')}: {item.get('skill')}")
            st.info(item.get("task"))
    else:
        st.success("No major missing skills. Focus on improving project impact.")
    
    st.subheader("Resume Quality Checks")

    quality_checks = result.get("quality_checks", [])

    if quality_checks:
        for check in quality_checks:
            st.warning(check)
    else:
        st.success("Resume quality looks good.")

    
    pdf_buffer = create_pdf_report(result)

    st.download_button(
        "Download PDF Report",
        data=pdf_buffer,
        file_name="resume_analysis_report.pdf",
        mime="application/pdf"
    )
    with st.expander("Interview Questions"):
        for question in result.get("interview_questions", []):
            st.info(question)