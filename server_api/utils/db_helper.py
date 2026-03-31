import sqlite3
import os

# =========================================================
# 🔥 DB PATH (RENDER + LOCAL SAFE)
# =========================================================
DB_PATH = os.getenv("DB_PATH", "licenses.db")

# 👉 ensure folder exists (important for render)
db_dir = os.path.dirname(DB_PATH)
if db_dir:
    os.makedirs(db_dir, exist_ok=True)

print("📂 USING DB PATH:", os.path.abspath(DB_PATH))


# =========================================================
# 🔌 GET CONNECTION
# =========================================================
def get_connection():
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row   # optional (clean dict access)
        return conn
    except Exception as e:
        print("❌ DB CONNECTION ERROR:", e)
        return None


# =========================================================
# 🔥 INIT DB (AUTO CREATE TABLE)
# =========================================================
def init_db():
    conn = get_connection()

    if conn is None:
        print("⚠ DB NOT CONNECTED → SKIP INIT")
        return

    try:
        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS licenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            license_key TEXT UNIQUE,
            machine_id TEXT,
            is_used INTEGER DEFAULT 0,
            expiry_date TEXT
        )
        """)

        conn.commit()
        print("✅ DB Initialized")

    except Exception as e:
        print("❌ INIT ERROR:", e)

    finally:
        conn.close()


# =========================================================
# 🔥 CREATE LICENSE
# =========================================================
def create_license(key, expiry):
    conn = get_connection()

    if conn is None:
        return {"status": "db_error"}

    try:
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO licenses (license_key, machine_id, is_used, expiry_date)
            VALUES (?, NULL, 0, ?)
        """, (key, expiry))

        conn.commit()

        print("✅ LICENSE CREATED:", key)
        return {"status": "created"}

    except Exception as e:
        print("❌ CREATE ERROR:", e)
        return {"status": "error"}

    finally:
        conn.close()


# =========================================================
# 🔍 GET LICENSE
# =========================================================
def get_license(key):
    conn = get_connection()

    if conn is None:
        return None

    try:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, license_key, machine_id, is_used, expiry_date
            FROM licenses
            WHERE license_key=?
        """, (key,))

        return cursor.fetchone()

    except Exception as e:
        print("❌ GET ERROR:", e)
        return None

    finally:
        conn.close()


# =========================================================
# 🔄 UPDATE LICENSE (ACTIVATE)
# =========================================================
def update_license(machine_id, key):
    conn = get_connection()

    if conn is None:
        return False

    try:
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE licenses
            SET machine_id=?, is_used=1
            WHERE license_key=?
        """, (machine_id, key))

        conn.commit()

        print("✅ LICENSE UPDATED:", key)
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

    if conn is None:
        return False

    try:
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE licenses
            SET machine_id=NULL, is_used=0
            WHERE license_key=?
        """, (key,))

        conn.commit()

        print("🔄 LICENSE RESET:", key)
        return True

    except Exception as e:
        print("❌ RESET ERROR:", e)
        return False

    finally:
        conn.close()