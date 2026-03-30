import sqlite3
import os

# 🔥 DB PATH (MATCH WITH db_helper)
db_path = "server_api/database/db.sqlite3"

os.makedirs(os.path.dirname(db_path), exist_ok=True)

conn = sqlite3.connect(db_path)
cur = conn.cursor()

# =========================================================
# 🔥 CORRECT TABLE (IMPORTANT)
# =========================================================
cur.execute("""
CREATE TABLE IF NOT EXISTS licenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    license_key TEXT UNIQUE,
    machine_id TEXT,
    is_used INTEGER DEFAULT 0,
    expiry_date TEXT
)
""")

# =========================================================
# 🔥 ADD TEST KEYS
# =========================================================
cur.execute("""
INSERT OR IGNORE INTO licenses (license_key, is_used)
VALUES ('LIC-TEST-001', 0)
""")

cur.execute("""
INSERT OR IGNORE INTO licenses (license_key, is_used)
VALUES ('LIC-ABC-12345', 0)
""")

conn.commit()
conn.close()

print("✅ DB + TABLE + TEST KEYS CREATED")