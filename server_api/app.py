from flask import Flask
from server_api.routes.license_routes import license_bp

app = Flask(__name__)

app.register_blueprint(license_bp, url_prefix="/api/license")

if __name__ == "__main__":
    app.run(debug=True)