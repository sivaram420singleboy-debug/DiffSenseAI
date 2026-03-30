from server_api.utils.db_helper import get_connection
import sqlite3

# 🔥 INIT DB
def init_db():
    conn = get_connection()
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
    conn.close()


# 🔥 CREATE LICENSE (WITH EXPIRY)
def create_license(key, expiry):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO licenses (license_key, is_used, machine_id, expiry_date)
            VALUES (?, 0, NULL, ?)
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

    cursor.execute(
        "SELECT * FROM licenses WHERE license_key=?",
        (key,)
    )

    row = cursor.fetchone()
    conn.close()

    print("🔎 Fetch License:", row)
    return row


# 🔥 UPDATE LICENSE (ACTIVATE)
def update_license(machine_id, key):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE licenses
        SET machine_id=?, is_used=1
        WHERE license_key=?
    """, (machine_id, key))

    conn.commit()
    conn.close()

    print("🔒 License Bound:", machine_id)


# 🔁 RESET (TESTING)
def reset_license(key):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE licenses
        SET machine_id=NULL, is_used=0
        WHERE license_key=?
    """, (key,))

    conn.commit()
    conn.close()