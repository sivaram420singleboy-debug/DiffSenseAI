import sqlite3
import os

# 🔥 SINGLE DB PATH (ONLY THIS)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "database", "db.sqlite3")

print("🔥 FINAL DB PATH:", DB_PATH)
print("🔥 MODEL DB:", DB_PATH)

def get_connection():
    try:
        conn = sqlite3.connect(DB_PATH)
        return conn
    except Exception as e:
        print("❌ DB CONNECTION ERROR:", e)
        return None