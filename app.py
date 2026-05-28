# =========================
# app.py
# =========================

import streamlit as st

from utils import (
    extract_pdf_text,
    extract_docx_text,
    clean_resume_text,
    extract_skills,
    calculate_ats_score,
    find_missing_skills,
    generate_suggestions,
    calculate_skill_match,
    generate_pdf_report,
    generate_ai_feedback
)

from database import (
    save_analysis,
    get_all_analysis,
    delete_all_analysis
)


def try_rerun():
    try:
        st.experimental_rerun()
    except AttributeError:
        pass


# =========================
# Page Config
# =========================

st.set_page_config(
    page_title="AI Resume Analyzer",
    layout="centered"
)

# =========================
# Custom CSS
# =========================

st.markdown(
    """
    <style>

    .main {
        background-color: #0E1117;
        color: white;
    }

    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 3em;
        background-color: #4CAF50;
        color: white;
        font-size: 18px;
    }

    .stTextArea textarea {
        border-radius: 10px;
    }

    .stFileUploader {
        border-radius: 10px;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# =========================
# Sidebar
# =========================

st.sidebar.title(
    "AI Resume Analyzer"
)

st.sidebar.write(
    "NLP-based ATS Resume Checker"
)

menu = st.sidebar.radio(
    "Navigation",
    [
        "Resume Analyzer",
        "Analysis History"
    ]
)

# =========================
# Resume Analyzer Page
# =========================

if menu == "Resume Analyzer":

    st.title("AI Resume Analyzer")

    st.markdown(
        """
        ### Smart AI-Powered Resume Screening System
        """
    )

    st.write(
        "Upload your resume and compare it with the job description."
    )

    # =========================
    # Upload Resume
    # =========================

    uploaded_resume = st.file_uploader(
        "Upload Resume",
        type=["pdf", "docx"]
    )

    # =========================
    # Job Description
    # =========================

    job_description = st.text_area(
        "Paste Job Description Here"
    )

    # =========================
    # Analyze Button
    # =========================

    if st.button("Analyze Resume"):

        with st.spinner(
            "Analyzing Resume..."
        ):

            # =========================
            # Validation
            # =========================

            if uploaded_resume is None:

                st.warning(
                    "Please upload a resume."
                )

            elif job_description.strip() == "":

                st.warning(
                    "Please enter job description."
                )

            else:

                try:

                    # =========================
                    # Extract Resume Text
                    # =========================

                    if (
                        uploaded_resume.type
                        == "application/pdf"
                    ):

                        resume_text = (
                            extract_pdf_text(
                                uploaded_resume
                            )
                        )

                    else:

                        resume_text = (
                            extract_docx_text(
                                uploaded_resume
                            )
                        )

                    # =========================
                    # Clean Resume
                    # =========================

                    cleaned_resume = (
                        clean_resume_text(
                            resume_text
                        )
                    )

                    # =========================
                    # Extract Skills
                    # =========================

                    resume_skills = (
                        extract_skills(
                            cleaned_resume
                        )
                    )

                    jd_skills = (
                        extract_skills(
                            job_description
                        )
                    )

                    # =========================
                    # ATS Score
                    # =========================

                    ats_score = (
                        calculate_ats_score(
                            cleaned_resume,
                            job_description
                        )
                    )

                    # =========================
                    # Skill Match
                    # =========================

                    skill_match = (
                        calculate_skill_match(
                            resume_skills,
                            jd_skills
                        )
                    )

                    # =========================
                    # Missing Skills
                    # =========================

                    missing_skills = (
                        find_missing_skills(
                            resume_skills,
                            jd_skills
                        )
                    )

                    # =========================
                    # Suggestions
                    # =========================

                    suggestions = (
                        generate_suggestions(
                            ats_score,
                            missing_skills
                        )
                    )

                    # =========================
                    # AI Feedback
                    # =========================

                    ai_feedback = (
                        generate_ai_feedback(
                            ats_score,
                            missing_skills
                        )
                    )

                    # =========================
                    # Resume Statistics
                    # =========================

                    word_count = len(
                        resume_text.split()
                    )

                    char_count = len(
                        resume_text
                    )

                    # =========================
                    # ATS Category
                    # =========================

                    if ats_score >= 85:

                        category = "Excellent"

                    elif ats_score >= 70:

                        category = "Good"

                    elif ats_score >= 50:

                        category = "Average"

                    else:

                        category = "Poor"

                    # =========================
                    # Resume Rank
                    # =========================

                    if ats_score >= 90:

                        rank = "A+"

                    elif ats_score >= 80:

                        rank = "A"

                    elif ats_score >= 70:

                        rank = "B"

                    elif ats_score >= 60:

                        rank = "C"

                    else:

                        rank = "D"

                    # =========================
                    # Save Analysis
                    # =========================

                    save_analysis(
                        ats_score,
                        category,
                        resume_skills,
                        missing_skills
                    )

                    # =========================
                    # Success Message
                    # =========================

                    st.success(
                        "Resume Processed Successfully"
                    )

                    # =========================
                    # ATS Dashboard
                    # =========================

                    st.subheader(
                        "ATS Score Dashboard"
                    )

                    st.metric(
                        "Resume Match Score",
                        f"{ats_score}%"
                    )

                    st.progress(
                        int(ats_score)
                    )

                    st.metric(
                        "Skill Match Percentage",
                        f"{skill_match}%"
                    )

                    st.metric(
                        "Resume Rank",
                        rank
                    )

                    # =========================
                    # ATS Category Message
                    # =========================

                    if ats_score >= 85:

                        st.success(
                            "Excellent ATS Match!"
                        )

                    elif ats_score >= 70:

                        st.warning(
                            "Good Match. Improve further."
                        )

                    elif ats_score >= 50:

                        st.warning(
                            "Average ATS Match."
                        )

                    else:

                        st.error(
                            "Low ATS Score."
                        )

                    st.write(
                        f"ATS Category: {category}"
                    )

                    st.divider()

                    # =========================
                    # Resume Text
                    # =========================

                    with st.expander(
                        "View Extracted Resume Text"
                    ):

                        st.text_area(
                            "Resume Content",
                            resume_text,
                            height=250
                        )

                    # =========================
                    # Cleaned Resume Text
                    # =========================

                    with st.expander(
                        "View Cleaned Resume Text"
                    ):

                        st.text_area(
                            "Cleaned Resume",
                            cleaned_resume,
                            height=250
                        )

                    # =========================
                    # Important Keywords
                    # =========================

                    st.subheader(
                        "Important Keywords"
                    )

                    for skill in resume_skills:

                        st.code(skill)

                    st.divider()

                    # =========================
                    # Tabs
                    # =========================

                    tab1, tab2, tab3 = st.tabs(

                        [
                            "Resume Stats",
                            "Skills",
                            "Suggestions"
                        ]
                    )

                    # =========================
                    # Resume Stats
                    # =========================

                    with tab1:

                        st.subheader(
                            "Resume Statistics"
                        )

                        st.write(
                            f"Total Words: {word_count}"
                        )

                        st.write(
                            f"Total Characters: {char_count}"
                        )

                    # =========================
                    # Skills Tab
                    # =========================

                    with tab2:

                        st.subheader(
                            "Detected Skills"
                        )

                        for skill in resume_skills:

                            st.success(skill)

                        st.subheader(
                            "Missing Skills"
                        )

                        if len(missing_skills) > 0:

                            for skill in missing_skills:

                                st.error(skill)

                        else:

                            st.success(
                                "No missing skills found."
                            )

                    # =========================
                    # Suggestions Tab
                    # =========================

                    with tab3:

                        st.subheader(
                            "Resume Suggestions"
                        )

                        for suggestion in suggestions:

                            st.info(suggestion)

                        st.subheader(
                            "AI Resume Feedback"
                        )

                        for feedback in ai_feedback:

                            st.success(feedback)

                    st.divider()

                    # =========================
                    # Pie Chart
                    # =========================

                    matched_count = len(
                        resume_skills
                    )

                    missing_count = len(
                        missing_skills
                    )

                    st.subheader(
                        "Skills Summary"
                    )

                    st.write(
                        f"Matched Skills: {matched_count}"
                    )

                    st.write(
                        f"Missing Skills: {missing_count}"
                    )

                    # =========================
                    # Bar Chart
                    # =========================

                    st.subheader(
                        "Resume Performance"
                    )

                    st.bar_chart(
                        {
                            "Score": [
                                ats_score,
                                skill_match
                            ]
                        }
                    )

                    st.divider()

                    # =========================
                    # Text Report
                    # =========================

                    report = f"""
ATS Score: {ats_score}%

ATS Category: {category}

Resume Rank: {rank}

Skill Match Percentage:
{skill_match}%

Detected Skills:
{', '.join(resume_skills)}

Missing Skills:
{', '.join(missing_skills)}

Suggestions:
{', '.join(suggestions)}
"""

                    st.download_button(

                        label="Download Text Report",

                        data=report,

                        file_name="resume_report.txt",

                        mime="text/plain"
                    )

                    # =========================
                    # PDF Report
                    # =========================

                    pdf_file = (
                        generate_pdf_report(

                            ats_score,
                            category,
                            rank,
                            skill_match,
                            resume_skills,
                            missing_skills,
                            suggestions
                        )
                    )

                    with open(
                        pdf_file,
                        "rb"
                    ) as pdf:

                        st.download_button(

                            label="Download PDF Report",

                            data=pdf,

                            file_name="resume_report.pdf",

                            mime="application/pdf"
                        )

                except Exception as e:

                    st.error(
                        f"Error processing file: {e}"
                    )

# =========================
# Analysis History
# =========================

elif menu == "Analysis History":

    st.title("Analysis History")

    try:

        records = get_all_analysis() or []

    except Exception as e:

        st.error(
            f"Unable to load analysis history: {e}"
        )

        records = []

    if not records:

        st.warning(
            "No analysis records found."
        )

    else:

        scores = []

        for record in records:

            if record and len(record) > 1 and record[1] is not None:

                try:

                    scores.append(float(record[1]))

                except (TypeError, ValueError):

                    continue

        if not scores:

            st.warning(
                "No valid ATS scores available in history."
            )

        else:

            # =========================
            # ATS History Chart
            # =========================

            st.subheader(
                "ATS Score History"
            )

            st.line_chart(
                {
                    "ATS Score": scores
                }
            )

            # =========================
            # Metrics
            # =========================

            average_score = sum(scores) / len(scores)

            highest_score = max(scores)

            st.metric(
                "Average ATS Score",
                f"{round(average_score, 2)}%"
            )

            st.metric(
                "Highest ATS Score",
                f"{highest_score}%"
            )

            st.divider()

        # =========================
        # Delete History
        # =========================

        with st.expander("Delete Total History"):

            st.write(
                "This will remove all saved analyses permanently."
            )

            confirm_delete = st.checkbox(
                "I understand this cannot be undone",
                key="confirm_delete_history"
            )

            if st.button("Delete All History", key="delete_all_history"):

                if confirm_delete:

                    try:

                        delete_all_analysis()

                        st.success(
                            "All analysis history has been deleted."
                        )

                        try_rerun()

                    except Exception as e:

                        st.error(
                            f"Failed to delete history: {e}"
                        )

                else:

                    st.warning(
                        "Please confirm deletion by checking the box before deleting."
                    )

        # =========================
        # Records
        # =========================

        for record in records:

            record = list(record) + [""] * (6 - len(record))

            ats_score = (
                f"{record[1]}%"
                if record[1] is not None and record[1] != ""
                else "N/A"
            )

            st.subheader(
                f"Analysis ID: {record[0]}"
            )

            st.write(
                f"ATS Score: {ats_score}"
            )

            st.write(
                f"Category: {record[2] or 'N/A'}"
            )

            st.write(
                f"Skills: {record[3] or 'N/A'}"
            )

            st.write(
                f"Missing Skills: {record[4] or 'N/A'}"
            )

            st.write(
                f"Timestamp: {record[5] or 'N/A'}"
            )

            st.divider()

            st.divider()

# =========================
# Footer
# =========================

st.divider()

st.caption(
    "AI Resume Analyzer using Python, NLP, and Streamlit"
)