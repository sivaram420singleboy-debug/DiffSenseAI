import sqlite3
import os

# 🔥 RENDER SAFE PATH
DB_PATH = os.getenv("DB_PATH", "/app/licenses.db")

def get_connection():
    try:
        conn = sqlite3.connect(DB_PATH)
        return conn
    except Exception as e:
        print("❌ DB CONNECTION ERROR:", e)
        return None