import sqlite3
import bcrypt

conn = sqlite3.connect("fake_jobs.db")
c = conn.cursor()

# ==================================================
# ADD is_admin COLUMN IF IT DOESN'T EXIST
# ==================================================

try:
    c.execute(
        "ALTER TABLE users ADD COLUMN is_admin INTEGER DEFAULT 0"
    )
    print("✅ is_admin column added")
except Exception:
    print("ℹ️ Column already exists, skipping")

# ==================================================
# DELETE admin1 IF EXISTS AND RECREATE CLEANLY
# ==================================================

c.execute(
    "DELETE FROM users WHERE username = ?",
    ("admin1",)
)
print("🗑️ Old admin1 deleted (if existed)")

password = "admin123"

hashed = bcrypt.hashpw(
    password.encode(),
    bcrypt.gensalt()
)

c.execute(
    "INSERT INTO users (username, password, is_admin) VALUES (?, ?, ?)",
    ("admin1", hashed, 1)
)
print("✅ admin1 created fresh")

conn.commit()
conn.close()

print("\n✅ Done! Login with:")
print("   Username : admin1")
print("   Password : admin123")
