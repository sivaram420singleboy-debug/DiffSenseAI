import os
import psycopg2

def get_connection():
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASS"),
            port=os.getenv("DB_PORT")
        )

        print("🔥 PostgreSQL Connected Successfully")
        return conn

    except Exception as e:
        print("❌ DB ERROR:", str(e))
        return None