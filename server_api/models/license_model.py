from server_api.utils.db_helper import get_connection


# 🔥 INIT DB (AUTO CREATE TABLE)
def init_db():
    conn = get_connection()
    cursor = conn.cursor()

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
    conn.close()
    print("✅ DB Initialized (PostgreSQL)")


# 🔥 CREATE LICENSE (WITH EXPIRY)
def create_license(key, expiry):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO licenses (license_key, is_used, machine_id, expiry_date)
            VALUES (%s, 0, NULL, %s)
        """, (key, expiry))

        conn.commit()
        print("✅ License Created:", key)

    except Exception as e:
        print("⚠ Error creating license:", e)

    finally:
        conn.close()


# 🔥 GET LICENSE
def get_license(key):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT id, license_key, machine_id, is_used, expiry_date 
            FROM licenses 
            WHERE license_key=%s
        """, (key,))

        row = cursor.fetchone()
        print("🔎 Fetch License:", row)

        return row

    except Exception as e:
        print("❌ DB ERROR:", e)
        return None

    finally:
        conn.close()


# 🔥 UPDATE LICENSE (ACTIVATE)
def update_license(machine_id, key):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            UPDATE licenses
            SET machine_id=%s, is_used=1
            WHERE license_key=%s
        """, (machine_id, key))

        conn.commit()
        print("🔒 License Bound:", machine_id)

    except Exception as e:
        print("❌ UPDATE ERROR:", e)

    finally:
        conn.close()


# 🔁 RESET LICENSE (TESTING ONLY)
def reset_license(key):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            UPDATE licenses
            SET machine_id=NULL, is_used=0
            WHERE license_key=%s
        """, (key,))

        conn.commit()
        print("♻ License Reset")

    except Exception as e:
        print("❌ RESET ERROR:", e)

    finally:
        conn.close()