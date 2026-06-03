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
# CREATE admin1 USER IF NOT EXISTS
# ==================================================

password = "admin123"  # Change this to your preferred password

hashed = bcrypt.hashpw(
    password.encode(),
    bcrypt.gensalt()
)

c.execute(
    "SELECT username FROM users WHERE username = ?",
    ("admin1",)
)

existing = c.fetchone()

if existing:
    c.execute(
        "UPDATE users SET is_admin = 1 WHERE username = 'admin1'"
    )
    print("✅ admin1 already exists — set as admin")
else:
    c.execute(
        "INSERT INTO users (username, password, is_admin) VALUES (?, ?, ?)",
        ("admin1", hashed, 1)
    )
    print("✅ admin1 created successfully")

conn.commit()
conn.close()

print("\n✅ Done! Login with:")
print("   Username : admin1")
print("   Password : admin123")
