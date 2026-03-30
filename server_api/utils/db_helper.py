import sqlite3
import os

# DB file path (auto create)
DB_PATH = os.path.join(os.getcwd(), "licenses.db")

def get_connection():
    try:
        conn = sqlite3.connect(DB_PATH)
        print("✅ SQLite DB CONNECTED")
        return conn
    except Exception as e:
        print("❌ DB ERROR:", e)
        return None