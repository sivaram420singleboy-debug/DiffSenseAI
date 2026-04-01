import psycopg2
import os

DATABASE_URL = os.getenv("DATABASE_URL")

# =========================================================
# 🔥 GET CONNECTION
# =========================================================
def get_connection():
    try:
        return psycopg2.connect(DATABASE_URL)
    except Exception as e:
        print("❌ DB ERROR:", e)
        return None

# =========================================================
# 🔥 CREATE LICENSE
# =========================================================
def create_license(key):
    conn = get_connection()
    if not conn:
        return {"status": "db_error"}

    try:
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO licenses (license_key)
            VALUES (%s)
            ON CONFLICT (license_key) DO NOTHING
        """, (key.strip(),))

        conn.commit()

        return {"status": "created"}

    except Exception as e:
        print("❌ CREATE ERROR:", e)
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
        cur = conn.cursor()

        cur.execute("""
            SELECT id, license_key, machine_id, status
            FROM licenses
            WHERE license_key=%s
        """, (key.strip(),))

        return cur.fetchone()

    except Exception as e:
        print("❌ GET ERROR:", e)
        return None

    finally:
        conn.close()

# =========================================================
# 🔥 ACTIVATE LICENSE
# =========================================================
def activate_license(machine_id, username, key):
    conn = get_connection()
    if not conn:
        return False

    try:
        cur = conn.cursor()

        cur.execute("""
            UPDATE licenses
            SET machine_id=%s,
                username=%s,
                status='Activated'
            WHERE license_key=%s
        """, (machine_id, username, key.strip()))

        conn.commit()

        return cur.rowcount > 0

    except Exception as e:
        print("❌ ACTIVATE ERROR:", e)
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
        cur = conn.cursor()

        cur.execute("""
            UPDATE licenses
            SET machine_id=NULL,
                username=NULL,
                status='Non-Activated'
            WHERE license_key=%s
        """, (key.strip(),))

        conn.commit()

        return True

    except Exception as e:
        print("❌ RESET ERROR:", e)
        return False

    finally:
        conn.close()