import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "database", "db.sqlite3")

def get_connection():
    try:
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        conn = sqlite3.connect(DB_PATH)
        print("✅ SQLite DB CONNECTED:", DB_PATH)
        return conn
    except Exception as e:
        print("❌ DB ERROR:", e)
        return None