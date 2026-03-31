from flask import Flask, jsonify
from server_api.routes.license_routes import license_bp
import os
import sqlite3

app = Flask(__name__)

# =========================================================
# 🔥 DATABASE PATH (RENDER SAFE FIX)
# =========================================================
# 👉 IMPORTANT: /app remove pannirukom
DB_PATH = "server_api/database/db.sqlite3"
print("📂 USING DB PATH:", DB_PATH)
print("🔥 APP DB:", DB_PATH)


# =========================================================
# 🔥 INIT DB (FINAL FIXED)
# =========================================================
def init_db():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS licenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            license_key TEXT UNIQUE,
            machine_id TEXT,
            is_used INTEGER DEFAULT 0
        )
        """)

        conn.commit()
        conn.close()

        print("✅ DB Created + Table Ready")

    except Exception as e:
        print("❌ DB INIT ERROR:", e)


# =========================================================
# 🔥 RUN DB INIT
# =========================================================
print("🚀 Initializing Database...")
init_db()


# =========================================================
# 🔗 REGISTER ROUTES
# =========================================================
app.register_blueprint(license_bp, url_prefix="/api/license")


# =========================================================
# 🏠 ROOT ROUTE
# =========================================================
@app.route("/")
def home():
    return jsonify({
        "message": "🚀 DiffSense AI License Server Running",
        "status": "ok",
        "db_path": DB_PATH
    })


# =========================================================
# ❤️ HEALTH CHECK
# =========================================================
@app.route("/health")
def health():
    return jsonify({"status": "healthy"})


# =========================================================
# 🔥 DEBUG ROUTE
# =========================================================
@app.route("/debug/licenses")
def debug_licenses():
    try:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()

        cur.execute("SELECT * FROM licenses")
        rows = cur.fetchall()

        conn.close()

        return jsonify({
            "count": len(rows),
            "data": rows
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        })


# =========================================================
# 🔥 ADD TEST LICENSE
# =========================================================
@app.route("/debug/add")
def add_test_key():
    try:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()

        cur.execute(
            "INSERT OR IGNORE INTO licenses (license_key) VALUES ('LIC-ABC-12345')"
        )

        conn.commit()
        conn.close()

        return jsonify({"status": "key added"})

    except Exception as e:
        return jsonify({"error": str(e)})


# =========================================================
# 🚀 RUN APP
# =========================================================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)