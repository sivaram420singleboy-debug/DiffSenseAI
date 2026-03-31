from server_api.utils.db_helper import get_connection
import os

# =========================================================
# 🔥 SINGLE DB SOURCE (SYNC WITH db_helper)
# =========================================================
DB_PATH = os.getenv("DB_PATH", "/opt/render/project/src/server_api/database/db.sqlite3")
print("📂 LICENSE MODEL DB:", DB_PATH)


# =========================================================
# 🔥 INIT DB (SAFE)
# =========================================================
def init_db():
    conn = get_connection()

    if conn is None:
        print("⚠ DB NOT CONNECTED → SKIPPING INIT")
        return

    cursor = conn.cursor()

    try:
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
        print("✅ SQLite DB Initialized")

    except Exception as e:
        print("❌ INIT ERROR:", e)

    finally:
        cursor.close()
        conn.close()


# =========================================================
# 🔥 CREATE LICENSE (FIXED + DEBUG)
# =========================================================
def create_license(key, expiry):
    conn = get_connection()

    if conn is None:
        print("❌ DB CONNECTION FAILED")
        return {"status": "db_error"}

    cursor = conn.cursor()

    try:
        print("📥 INSERTING:", key, expiry)

        cursor.execute("""
            INSERT INTO licenses (license_key, is_used, machine_id, expiry_date)
            VALUES (?, 0, NULL, ?)
        """, (key.strip(), expiry))

        conn.commit()

        print("✅ LICENSE CREATED:", key)

        return {"status": "created"}

    except Exception as e:
        print("❌ INSERT ERROR:", e)
        return {"status": "error"}

    finally:
        cursor.close()
        conn.close()


# =========================================================
# 🔥 GET LICENSE (FIXED)
# =========================================================
def get_license(key):
    conn = get_connection()

    if conn is None:
        return None

    cursor = conn.cursor()

    try:
        clean_key = key.strip()

        print("🔍 SEARCHING KEY:", clean_key)

        cursor.execute("""
            SELECT id, license_key, machine_id, is_used, expiry_date 
            FROM licenses 
            WHERE license_key=?
        """, (clean_key,))

        result = cursor.fetchone()

        print("📊 DB RESULT:", result)

        return result

    except Exception as e:
        print("❌ DB ERROR:", e)
        return None

    finally:
        cursor.close()
        conn.close()


# =========================================================
# 🔥 UPDATE LICENSE
# =========================================================
def update_license(machine_id, key):
    conn = get_connection()

    if conn is None:
        return False

    cursor = conn.cursor()

    try:
        clean_key = key.strip()

        print("🔄 UPDATING LICENSE:", clean_key)

        cursor.execute("""
            UPDATE licenses
            SET machine_id=?, is_used=1
            WHERE license_key=?
        """, (machine_id, clean_key))

        conn.commit()

        print("✅ LICENSE ACTIVATED")

        return True

    except Exception as e:
        print("❌ UPDATE ERROR:", e)
        return False

    finally:
        cursor.close()
        conn.close()


# =========================================================
# 🔁 RESET LICENSE
# =========================================================
def reset_license(key):
    conn = get_connection()

    if conn is None:
        return False

    cursor = conn.cursor()

    try:
        clean_key = key.strip()

        print("♻ RESET LICENSE:", clean_key)

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
        cursor.close()
        conn.close()