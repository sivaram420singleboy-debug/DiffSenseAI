from flask import Flask, jsonify
from server_api.routes.license_routes import license_bp
from server_api.models.license_model import init_db

app = Flask(__name__)

# 🔥 INIT DATABASE (VERY IMPORTANT)
init_db()

# 🔗 REGISTER ROUTES
app.register_blueprint(license_bp, url_prefix="/api/license")


# 🔥 ROOT ROUTE (404 avoid + test)
@app.route("/")
def home():
    return jsonify({
        "message": "🚀 DiffSense AI License Server Running",
        "status": "ok"
    })


# 🔥 HEALTH CHECK (Render friendly)
@app.route("/health")
def health():
    return jsonify({"status": "healthy"})


# ▶ RUN (LOCAL)
if __name__ == "__main__":
    app.run(debug=True)