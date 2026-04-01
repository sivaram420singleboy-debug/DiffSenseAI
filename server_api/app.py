from flask import Flask, jsonify
from server_api.routes.license_routes import license_bp
import os
import psycopg2

app = Flask(__name__)

# =========================================================
# 🔥 DATABASE URL (RENDER)
# =========================================================
DATABASE_URL = os.getenv("DATABASE_URL")

print("🔥 USING POSTGRES DB:", DATABASE_URL)

# =========================================================
# 🔥 CREATE TABLE
# =========================================================
def create_table():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()

        cur.execute("""
        CREATE TABLE IF NOT EXISTS licenses (
            id SERIAL PRIMARY KEY,
            license_key TEXT UNIQUE,
            status TEXT DEFAULT 'Non-Activated',
            machine_id TEXT,
            username TEXT,
            company TEXT,
            activated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        conn.commit()
        cur.close()
        conn.close()

        print("✅ POSTGRES TABLE READY")

    except Exception as e:
        print("❌ DB ERROR:", e)

# INIT
create_table()

# =========================================================
# ROUTES
# =========================================================
app.register_blueprint(license_bp, url_prefix="/api/license")

# =========================================================
# ROOT
# =========================================================
@app.route("/")
def home():
    return jsonify({
        "message": "🚀 License Server Running",
        "db": "PostgreSQL Connected"
    })

# =========================================================
# HEALTH
# =========================================================
@app.route("/health")
def health():
    return jsonify({"status": "ok"})

# =========================================================
# DEBUG
# =========================================================
@app.route("/debug/licenses")
def debug():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()

        cur.execute("SELECT * FROM licenses")
        rows = cur.fetchall()

        cur.close()
        conn.close()

        return jsonify({
            "source": "POSTGRES ✅",
            "count": len(rows),
            "data": rows
        })

    except Exception as e:
        return jsonify({"error": str(e)})

# =========================================================
# ADD TEST KEY
# =========================================================
@app.route("/debug/add")
def add():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()

        cur.execute("""
        INSERT INTO licenses (license_key)
        VALUES ('DSAI-TEST-001')
        ON CONFLICT (license_key) DO NOTHING
        """)

        conn.commit()
        cur.close()
        conn.close()

        return jsonify({"status": "added"})

    except Exception as e:
        return jsonify({"error": str(e)})

# =========================================================
# RUN
# =========================================================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)