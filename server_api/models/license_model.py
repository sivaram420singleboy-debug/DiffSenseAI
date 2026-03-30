from server_api.utils.db_helper import get_connection


# =========================================================
# 🔥 INIT DB (SAFE - NO CRASH)
# =========================================================
def init_db():
    conn = get_connection()

    if conn is None:
        print("⚠ DB NOT CONNECTED → SKIPPING INIT")
        return   # ❗ IMPORTANT (no crash)

    cursor = conn.cursor()

    try:
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS licenses (
            id SERIAL PRIMARY KEY,
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
        cursor.close()
        conn.close()


# =========================================================
# 🔥 CREATE LICENSE
# =========================================================
def create_license(key, expiry):
    conn = get_connection()

    if conn is None:
        return {"status": "db_error"}

    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO licenses (license_key, is_used, machine_id, expiry_date)
            VALUES (%s, 0, NULL, %s)
        """, (key, expiry))

        conn.commit()
        return {"status": "created"}

    except Exception as e:
        print("⚠ Error creating license:", e)
        return {"status": "error"}

    finally:
        cursor.close()
        conn.close()


# =========================================================
# 🔥 GET LICENSE
# =========================================================
def get_license(key):
    conn = get_connection()

    if conn is None:
        return None

    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT id, license_key, machine_id, is_used, expiry_date 
            FROM licenses 
            WHERE license_key=%s
        """, (key,))

        return cursor.fetchone()

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
        cursor.execute("""
            UPDATE licenses
            SET machine_id=%s, is_used=1
            WHERE license_key=%s
        """, (machine_id, key))

        conn.commit()
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
        cursor.execute("""
            UPDATE licenses
            SET machine_id=NULL, is_used=0
            WHERE license_key=%s
        """, (key,))

        conn.commit()
        return True

    except Exception as e:
        print("❌ RESET ERROR:", e)
        return False

    finally:
        cursor.close()
        conn.close()