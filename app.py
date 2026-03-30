from flask import Flask, jsonify
from server_api.routes.license_routes import license_bp
from server_api.models.license_model import init_db
import os

app = Flask(__name__)

# 🔥 INIT DB
init_db()

# 🔗 ROUTES
app.register_blueprint(license_bp, url_prefix="/api/license")


@app.route("/")
def home():
    return jsonify({
        "message": "🚀 DiffSense AI License Server Running",
        "status": "ok"
    })


@app.route("/health")
def health():
    return jsonify({"status": "healthy"})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)