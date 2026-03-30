import sqlite3
import os

db_path = "server_api/database/db.sqlite3"

os.makedirs(os.path.dirname(db_path), exist_ok=True)

conn = sqlite3.connect(db_path)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS Licenses(
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    LicenseKey TEXT UNIQUE,
    MachineId TEXT,
    IsUsed INTEGER DEFAULT 0,
    ExpiryDate TEXT
)
""")

# 🔥 ADD TEST KEYS
cur.execute("INSERT OR IGNORE INTO Licenses (LicenseKey, IsUsed) VALUES ('LIC-ABC-12345', 0)")
cur.execute("INSERT OR IGNORE INTO Licenses (LicenseKey, IsUsed) VALUES ('LIC-TEST-11111', 0)")

conn.commit()
conn.close()

print("✅ DB created correctly")