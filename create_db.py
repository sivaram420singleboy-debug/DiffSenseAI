def get_connection():
    try:
        conn = psycopg2.connect(
            host=os.environ.get("DB_HOST"),
            database=os.environ.get("DB_NAME"),
            user=os.environ.get("DB_USER"),
            password=os.environ.get("DB_PASS"),
            port=os.environ.get("DB_PORT")
        )

        print("🔥 PostgreSQL Connected Successfully")
        return conn

    except Exception as e:
        print("❌ DB CONNECTION ERROR:", e)
        raise e   # 🔥 CRASH HERE DIRECTLY (GOOD)