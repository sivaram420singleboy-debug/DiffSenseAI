from flask import Flask, jsonify
from server_api.routes.license_routes import license_bp
import os
import sqlite3

app = Flask(__name__)

# =========================================================
# 🔥 DATABASE PATH (FINAL SAFE)
# =========================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database", "db.sqlite3")

print("📂 USING DB PATH:", DB_PATH)

# =========================================================
# 🔥 INIT DB
# =========================================================
def init_db():
    try:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()

        cur.execute("""
        CREATE TABLE IF NOT EXISTS licenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            license_key TEXT UNIQUE,
            status TEXT DEFAULT 'Non-Activated',
            machine_id TEXT,
            username TEXT,
            company TEXT,
            activated_at TEXT
        )
        """)

        conn.commit()
        conn.close()

        print("✅ DB Ready")

    except Exception as e:
        print("❌ DB ERROR:", e)


# =========================================================
# 🔥 INIT CALL
# =========================================================
print("🚀 Initializing DB...")
init_db()

# =========================================================
# 🔗 ROUTES
# =========================================================
app.register_blueprint(license_bp, url_prefix="/api/license")

# =========================================================
# 🏠 ROOT
# =========================================================
@app.route("/")
def home():
    return jsonify({
        "message": "🚀 License Server Running",
        "db": DB_PATH
    })

# =========================================================
# ❤️ HEALTH
# =========================================================
@app.route("/health")
def health():
    return jsonify({"status": "ok"})

# =========================================================
# 🔥 DEBUG
# =========================================================
@app.route("/debug/licenses")
def debug():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("SELECT * FROM licenses")
    data = cur.fetchall()

    conn.close()

    return jsonify({"data": data})


# =========================================================
# ➕ ADD KEY
# =========================================================
@app.route("/debug/add")
def add():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("INSERT OR IGNORE INTO licenses (license_key) VALUES ('DSAI-TEST-001')")

    conn.commit()
    conn.close()

    return jsonify({"status": "added"})


# =========================================================
# 🚀 RUN
# =========================================================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
    
print("🚀 INIT DB...")
init_db()