import sqlite3
import os

# =========================================================
# 🔥 DB PATH (LOCAL + RENDER SAFE)
# =========================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.getenv(
    "DB_PATH",
    os.path.join(BASE_DIR, "..", "database", "db.sqlite3")
)

DB_PATH = os.path.abspath(DB_PATH)

print("📂 LICENSE MODEL DB:", DB_PATH)


# =========================================================
# 🔥 GET CONNECTION (SAFE)
# =========================================================
def get_connection():
    try:
        conn = sqlite3.connect(DB_PATH)
        return conn
    except Exception as e:
        print("❌ DB CONNECTION ERROR:", e)
        return None


# =========================================================
# 🔥 INIT DB
# =========================================================
def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS licenses (
        id SERIAL PRIMARY KEY,
        license_key TEXT UNIQUE,
        machine_id TEXT,
        is_used INTEGER DEFAULT 0,
        expiry_date TEXT,
        activated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    cur.close()
    conn.close()

    print("✅ POSTGRES TABLE READY")


# =========================================================
# 🔥 CREATE LICENSE
# =========================================================
def create_license(key, expiry):
    conn = get_connection()

    if not conn:
        return {"status": "db_error"}

    try:
        cursor = conn.cursor()

        clean_key = key.strip()

        print("📥 INSERT:", clean_key, expiry)

        cursor.execute("""
            INSERT INTO licenses (license_key, machine_id, is_used, expiry_date)
            VALUES (?, NULL, 0, ?)
        """, (clean_key, expiry))

        conn.commit()

        return {"status": "created"}

    except sqlite3.IntegrityError:
        return {"status": "exists"}

    except Exception as e:
        print("❌ INSERT ERROR:", e)
        return {"status": "error"}

    finally:
        conn.close()


# =========================================================
# 🔥 GET LICENSE
# =========================================================
def get_license(key):
    conn = get_connection()

    if not conn:
        return None

    try:
        cursor = conn.cursor()

        clean_key = key.strip()

        print("🔍 FIND:", clean_key)

        cursor.execute("""
            SELECT id, license_key, machine_id, is_used, expiry_date
            FROM licenses
            WHERE license_key=?
        """, (clean_key,))

        result = cursor.fetchone()

        print("📊 RESULT:", result)

        return result

    except Exception as e:
        print("❌ GET ERROR:", e)
        return None

    finally:
        conn.close()


# =========================================================
# 🔥 UPDATE LICENSE (ACTIVATE)
# =========================================================
def update_license(machine_id, key):
    conn = get_connection()

    if not conn:
        return False

    try:
        cursor = conn.cursor()

        clean_key = key.strip()

        print("🔄 ACTIVATE:", clean_key)

        cursor.execute("""
            UPDATE licenses
            SET machine_id=?, is_used=1
            WHERE license_key=?
        """, (machine_id, clean_key))

        conn.commit()

        if cursor.rowcount == 0:
            print("⚠ NO ROW UPDATED")
            return False

        print("✅ ACTIVATED")

        return True

    except Exception as e:
        print("❌ UPDATE ERROR:", e)
        return False

    finally:
        conn.close()


# =========================================================
# 🔁 RESET LICENSE
# =========================================================
def reset_license(key):
    conn = get_connection()

    if not conn:
        return False

    try:
        cursor = conn.cursor()

        clean_key = key.strip()

        print("♻ RESET:", clean_key)

        cursor.execute("""
            UPDATE licenses
            SET machine_id=NULL, is_used=0
            WHERE license_key=?
        """, (clean_key,))

        conn.commit()

        return True

    except Exception as e:
        print("❌ RESET ERROR:", e)
        return False

    finally:
        conn.close()