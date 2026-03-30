from flask import Flask, jsonify
from server_api.routes.license_routes import license_bp
from server_api.models.license_model import init_db
import os

app = Flask(__name__)

# =========================================================
# 🔥 DATABASE PATH FIX (IMPORTANT)
# =========================================================
# 👉 Renderல persistent path use பண்ணணும்
DB_PATH = os.getenv("DB_PATH", "/app/licenses.db")

print("📂 USING DB PATH:", DB_PATH)

# =========================================================
# 🔥 SAFE DB INIT (NO CRASH IN RENDER)
# =========================================================
try:
    print("🚀 Initializing Database...")
    init_db(DB_PATH)   # ✅ path pass பண்ணுறோம்
    print("✅ DB Ready")
except Exception as e:
    print("⚠ DB INIT FAILED:", e)

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
        "db_path": DB_PATH   # 🔥 debugக்கு useful
    })

# =========================================================
# ❤️ HEALTH CHECK (RENDER)
# =========================================================
@app.route("/health")
def health():
    return jsonify({"status": "healthy"})

# =========================================================
# 🔥 DEBUG ROUTE (CHECK KEYS)
# =========================================================
@app.route("/debug/licenses")
def debug_licenses():
    import sqlite3
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
        return jsonify({"error": str(e)})

# =========================================================
# 🚀 RUN APP
# =========================================================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)