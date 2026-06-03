import sqlite3

# ==================================================
# DATABASE NAME
# ==================================================

DB_NAME = "fake_jobs.db"

# ==================================================
# CONNECT DATABASE
# ==================================================

def connect():

    return sqlite3.connect(DB_NAME)

# ==================================================
# INITIALIZE DATABASE
# ==================================================

def init_db():

    conn = connect()

    c = conn.cursor()

    # ==============================================
    # USERS TABLE
    # ==============================================

    c.execute("""
    CREATE TABLE IF NOT EXISTS users(
        username TEXT PRIMARY KEY,
        password TEXT,
        is_admin INTEGER DEFAULT 0
    )
    """)

    # ==============================================
    # HISTORY TABLE
    # ==============================================

    c.execute("""
    CREATE TABLE IF NOT EXISTS history(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        username TEXT,

        job_text TEXT,

        ml_score REAL,

        rule_score REAL,

        hybrid_score REAL,

        verdict TEXT
    )
    """)

    conn.commit()

    conn.close()

# ==================================================
# SAVE HISTORY
# ==================================================

def save_history(
    username,
    job_text,
    ml_score,
    rule_score,
    hybrid_score,
    verdict
):

    conn = connect()

    c = conn.cursor()

    c.execute("""
    INSERT INTO history(

        username,
        job_text,
        ml_score,
        rule_score,
        hybrid_score,
        verdict

    )

    VALUES (?, ?, ?, ?, ?, ?)
    """, (

        username,
        job_text,
        ml_score,
        rule_score,
        hybrid_score,
        verdict

    ))

    conn.commit()

    conn.close()

# ==================================================
# GET USER HISTORY
# ==================================================

def get_history(username):

    conn = connect()

    c = conn.cursor()

    c.execute("""
    SELECT

        job_text,
        ml_score,
        rule_score,
        hybrid_score,
        verdict

    FROM history

    WHERE username=?

    ORDER BY id DESC
    """, (username,))

    data = c.fetchall()

    conn.close()

    return data

# ==================================================
# CHECK IF USER IS ADMIN
# ==================================================

def is_user_admin(username):

    conn = connect()

    c = conn.cursor()

    c.execute("""
    SELECT is_admin FROM users WHERE username=?
    """, (username,))

    result = c.fetchone()

    conn.close()

    if result:
        return result[0] == 1

    return False

# ==================================================
# GET ALL HISTORY (ADMIN)
# ==================================================

def get_all_history():

    conn = connect()

    c = conn.cursor()

    c.execute("""
    SELECT

        username,
        job_text,
        ml_score,
        rule_score,
        hybrid_score,
        verdict

    FROM history

    ORDER BY id DESC
    """)

    data = c.fetchall()

    conn.close()

    return data