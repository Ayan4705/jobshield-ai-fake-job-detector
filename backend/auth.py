import sqlite3
import bcrypt

from backend.database import DB_NAME

# ==================================================
# REGISTER
# ==================================================

def register(username, password):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT username FROM users WHERE username=?",
        (username,)
    )

    existing_user = cursor.fetchone()

    if existing_user:
        conn.close()
        return False

    hashed = bcrypt.hashpw(
        password.encode(),
        bcrypt.gensalt()
    )

    cursor.execute(
        "INSERT INTO users (username, password) VALUES (?, ?)",
        (username, hashed)
    )

    conn.commit()
    conn.close()

    return True


# ==================================================
# LOGIN
# ==================================================

def login(username, password):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT password FROM users WHERE username=?",
        (username,)
    )

    result = cursor.fetchone()

    conn.close()

    if result:

        stored_password = result[0]

        return bcrypt.checkpw(
            password.encode(),
            stored_password
        )

    return False