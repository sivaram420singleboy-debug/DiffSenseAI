from flask import Flask, jsonify
from server_api.routes.license_routes import license_bp
from server_api.models.license_model import init_db
import os

app = Flask(__name__)

# =========================================================
# 🔥 SAFE DB INIT (NO CRASH IN RENDER)
# =========================================================
try:
    print("🚀 Initializing Database...")
    init_db()
    print("✅ DB Ready")
except Exception as e:
    print("⚠ DB INIT FAILED (will retry later):", e)

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
        "status": "ok"
    })

# =========================================================
# ❤️ HEALTH CHECK (RENDER)
# =========================================================
@app.route("/health")
def health():
    return jsonify({"status": "healthy"})

# =========================================================
# 🚀 RUN APP
# =========================================================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)