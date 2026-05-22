# =========================
# utils.py
# =========================

import PyPDF2

from docx import Document

import spacy

from sklearn.feature_extraction.text import (
    TfidfVectorizer
)

from sklearn.metrics.pairwise import (
    cosine_similarity
)

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import (
    getSampleStyleSheet
)

# =========================
# Load spaCy Model
# =========================

import spacy

try:

    nlp = spacy.load(
        "en_core_web_sm"
    )

except:

    from spacy.cli import download

    download("en_core_web_sm")

    nlp = spacy.load(
        "en_core_web_sm"
    )

# =========================
# PDF Extraction
# =========================

def extract_pdf_text(pdf_file):

    text = ""

    reader = PyPDF2.PdfReader(pdf_file)

    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:

            text += page_text

    return text

# =========================
# DOCX Extraction
# =========================

def extract_docx_text(docx_file):

    doc = Document(docx_file)

    text = ""

    for para in doc.paragraphs:

        text += para.text + "\n"

    return text

# =========================
# Clean Resume Text
# =========================

def clean_resume_text(text):

    doc = nlp(text)

    cleaned_words = []

    for token in doc:

        if (
            not token.is_stop
            and not token.is_punct
            and not token.is_space
        ):

            cleaned_words.append(
                token.text.lower()
            )

    cleaned_text = " ".join(
        cleaned_words
    )

    return cleaned_text

# =========================
# Skills Database
# =========================

SKILLS_DB = [

    "python",
    "java",
    "c",
    "c++",
    "sql",
    "html",
    "css",
    "javascript",
    "react",
    "nodejs",
    "mongodb",
    "mysql",

    "machine learning",
    "deep learning",
    "nlp",
    "data science",
    "tensorflow",
    "pytorch",

    "aws",
    "docker",
    "git",
    "github",
    "linux",
    "kubernetes",

    "django",
    "flask",
    "streamlit",

    "excel",
    "power bi",
    "tableau",

    "communication",
    "leadership",
    "teamwork"
]

# =========================
# Extract Skills
# =========================

def extract_skills(text):

    doc = nlp(text.lower())

    tokens = [
        token.text for token in doc
    ]

    found_skills = set()

    for skill in SKILLS_DB:

        skill_words = skill.lower().split()

        # Single Word Skills
        if len(skill_words) == 1:

            if skill.lower() in tokens:

                found_skills.add(skill)

        # Multi Word Skills
        else:

            if skill.lower() in text.lower():

                found_skills.add(skill)

    return list(found_skills)

# =========================
# ATS Score
# =========================

def calculate_ats_score(
    resume_text,
    job_description
):

    text = [
        resume_text,
        job_description
    ]

    tfidf = TfidfVectorizer()

    matrix = tfidf.fit_transform(text)

    similarity = cosine_similarity(
        matrix
    )

    score = similarity[0][1] * 100

    return round(score, 2)

# =========================
# Missing Skills
# =========================

def find_missing_skills(
    resume_skills,
    jd_skills
):

    missing = []

    for skill in jd_skills:

        if skill not in resume_skills:

            missing.append(skill)

    return missing

# =========================
# Suggestions
# =========================

def generate_suggestions(
    ats_score,
    missing_skills
):

    suggestions = []

    if ats_score < 50:

        suggestions.append(
            "Resume has low ATS match."
        )

        suggestions.append(
            "Add more keywords from job description."
        )

    if len(missing_skills) > 0:

        suggestions.append(
            "Add missing technical skills."
        )

    suggestions.append(
        "Use strong action verbs."
    )

    suggestions.append(
        "Add measurable achievements."
    )

    suggestions.append(
        "Improve project descriptions."
    )

    return suggestions

# =========================
# Skill Match
# =========================

def calculate_skill_match(
    resume_skills,
    jd_skills
):

    if len(jd_skills) == 0:

        return 0

    matched = 0

    for skill in jd_skills:

        if skill in resume_skills:

            matched += 1

    score = (
        matched / len(jd_skills)
    ) * 100

    return round(score, 2)

# =========================
# PDF Report
# =========================

def generate_pdf_report(

    ats_score,
    category,
    rank,
    skill_match,
    resume_skills,
    missing_skills,
    suggestions
):

    file_name = "resume_report.pdf"

    doc = SimpleDocTemplate(
        file_name
    )

    styles = getSampleStyleSheet()

    elements = []

    title = Paragraph(
        "AI Resume Analysis Report",
        styles['Title']
    )

    elements.append(title)

    elements.append(
        Spacer(1, 12)
    )

    ats = Paragraph(
        f"<b>ATS Score:</b> {ats_score}%",
        styles['BodyText']
    )

    elements.append(ats)

    cat = Paragraph(
        f"<b>Category:</b> {category}",
        styles['BodyText']
    )

    elements.append(cat)

    rank_text = Paragraph(
        f"<b>Resume Rank:</b> {rank}",
        styles['BodyText']
    )

    elements.append(rank_text)

    sm = Paragraph(
        f"<b>Skill Match:</b> {skill_match}%",
        styles['BodyText']
    )

    elements.append(sm)

    elements.append(
        Spacer(1, 12)
    )

    skills_para = Paragraph(
        f"<b>Detected Skills:</b> {', '.join(resume_skills)}",
        styles['BodyText']
    )

    elements.append(skills_para)

    missing_para = Paragraph(
        f"<b>Missing Skills:</b> {', '.join(missing_skills)}",
        styles['BodyText']
    )

    elements.append(missing_para)

    elements.append(
        Spacer(1, 12)
    )

    suggestions_text = (
        "<br/>".join(suggestions)
    )

    sugg_para = Paragraph(
        f"<b>Suggestions:</b><br/>{suggestions_text}",
        styles['BodyText']
    )

    elements.append(sugg_para)

    doc.build(elements)

    return file_name

# =========================
# AI Feedback
# =========================

def generate_ai_feedback(

    ats_score,
    missing_skills
):

    feedback = []

    if ats_score >= 85:

        feedback.append(
            "Your resume is highly optimized for ATS systems."
        )

    elif ats_score >= 70:

        feedback.append(
            "Your resume is strong but can still improve."
        )

    else:

        feedback.append(
            "Your resume needs optimization for better ATS performance."
        )

    if len(missing_skills) > 0:

        feedback.append(
            "Focus on adding the missing technical skills."
        )

    feedback.append(
        "Add more measurable achievements in projects."
    )

    feedback.append(
        "Use concise and impactful descriptions."
    )

    return feedback