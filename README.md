**Project**

AI Resume Analyzer

**Description**

Lightweight Streamlit app that analyzes resumes against a job description, calculates an ATS score, extracts skills (spaCy), and generates PDF reports.

**Files**

- **Main**: [app.py](app.py) — Streamlit application entrypoint.
- **Helpers**: [utils.py](utils.py) — text extraction, NLP, scoring, and report generation.
- **Storage**: [database.py](database.py) — SQLite persistence for analysis history.
- **Dependencies**: [requirements.txt](requirements.txt)

**Requirements**

- **Python** 3.10+ recommended.
- See `requirements.txt` for the Python packages used.

**Setup**

1. Create and activate a virtual environment (Windows PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

2. (Optional) If you use Command Prompt instead of PowerShell, run `\.venv\Scripts\activate`.

**Run**

Start the Streamlit app:

```powershell
streamlit run app.py
```

**Notes**

- The app uses spaCy's `en_core_web_sm` model — install it with `python -m spacy download en_core_web_sm`.
- A small compatibility helper `try_rerun()` was added to `app.py` to avoid errors on newer Streamlit versions where `st.experimental_rerun` may be unavailable.

**Troubleshooting**

- If you see errors related to missing packages, re-run `pip install -r requirements.txt` inside the activated virtual environment.# AI Resume Analyzer

AI-powered resume analysis system using Python, NLP, and Streamlit.

## Features
- ATS score
- Skill extraction
- Missing skills detection
- Resume suggestions