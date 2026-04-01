import psycopg2
import os

# 🔥 GET DATABASE URL FROM RENDER ENV
DATABASE_URL = os.getenv("DATABASE_URL")

print("🔥 USING POSTGRES DB:", DATABASE_URL)

def get_connection():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        return conn
    except Exception as e:
        print("❌ DB CONNECTION ERROR:", e)
        return None