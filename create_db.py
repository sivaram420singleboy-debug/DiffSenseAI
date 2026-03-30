import sqlite3

conn = sqlite3.connect("server_api/database/db.sqlite3")
cur = conn.cursor()

# ✅ CREATE TABLE CORRECT STRUCTURE
cur.execute("""
CREATE TABLE IF NOT EXISTS Licenses(
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    LicenseKey TEXT UNIQUE,
    MachineId TEXT,
    IsUsed INTEGER DEFAULT 0
)
""")

# ✅ INSERT KEYS
cur.execute("INSERT OR IGNORE INTO Licenses (LicenseKey, IsUsed) VALUES ('LIC-ABC-12345', 0)")
cur.execute("INSERT OR IGNORE INTO Licenses (LicenseKey, IsUsed) VALUES ('LIC-TEST-11111', 0)")

conn.commit()
conn.close()

print("✅ Database created + Keys added")