# =========================
# database.py
# =========================

import sqlite3

# =========================
# Database Connection
# =========================

conn = sqlite3.connect(
    "resume_analyzer.db",
    check_same_thread=False
)

cursor = conn.cursor()

# =========================
# Create Table
# =========================

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS analysis_history (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        ats_score REAL,

        category TEXT,

        skills TEXT,

        missing_skills TEXT,

        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """
)

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS analysis_sequence (

        name TEXT PRIMARY KEY,

        last_id INTEGER
    )
    """
)

conn.commit()

# =========================
# Sequence Management
# =========================

def get_next_analysis_id():

    cursor.execute(
        "INSERT OR IGNORE INTO analysis_sequence (name, last_id) VALUES ('analysis_history', 0)"
    )

    conn.commit()

    cursor.execute(
        "SELECT last_id FROM analysis_sequence WHERE name = 'analysis_history'"
    )

    row = cursor.fetchone()

    last_id = row[0] if row else 0

    if last_id == 0:

        cursor.execute(
            "SELECT MAX(id) FROM analysis_history"
        )

        max_id = cursor.fetchone()[0]

        if max_id is not None:

            last_id = max_id

            cursor.execute(
                "UPDATE analysis_sequence SET last_id = ? WHERE name = 'analysis_history'",
                (last_id,)
            )

            conn.commit()

    next_id = last_id + 1

    cursor.execute(
        "UPDATE analysis_sequence SET last_id = ? WHERE name = 'analysis_history'",
        (next_id,)
    )

    conn.commit()

    return next_id

# =========================
# Save Analysis
# =========================

def save_analysis(

    ats_score,
    category,
    skills,
    missing_skills
):

    analysis_id = get_next_analysis_id()

    cursor.execute(
        """
        INSERT INTO analysis_history
        (
            id,
            ats_score,
            category,
            skills,
            missing_skills
        )

        VALUES (?, ?, ?, ?, ?)
        """,
        (
            analysis_id,
            ats_score,
            category,
            ", ".join(skills),
            ", ".join(missing_skills)
        )
    )

    conn.commit()

# =========================
# Fetch Records
# =========================

def get_all_analysis():

    cursor.execute(
        """
        SELECT * FROM analysis_history
        """
    )

    data = cursor.fetchall()

    return data

# =========================
# Delete Analysis History
# =========================

def delete_all_analysis():

    cursor.execute(
        """
        DELETE FROM analysis_history
        """
    )

    conn.commit()