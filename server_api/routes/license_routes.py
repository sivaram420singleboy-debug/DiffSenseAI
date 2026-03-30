from flask import Blueprint, request, jsonify
from server_api.models.license_model import get_license, update_license, create_license
import os
import uuid
from datetime import datetime, timedelta

license_bp = Blueprint("license", __name__)

# 🔥 DB DEBUG
print("🔥 USING DB:", os.path.abspath("server_api/database/db.sqlite3"))


# =========================================================
# 🏠 ROOT CHECK (OPTIONAL BUT USEFUL)
# =========================================================
@license_bp.route("/", methods=["GET"])
def home():
    return jsonify({
        "status": "ok",
        "message": "DiffSense AI License API Running 🚀"
    })


# =========================================================
# 🔑 ACTIVATE LICENSE
# =========================================================
@license_bp.route("/activate", methods=["GET", "POST"])
def activate():
    try:
        # 🔥 SUPPORT BOTH METHODS
        if request.method == "GET":
            key = request.args.get("LicenseKey")
            machine = request.args.get("MachineId")
        else:
            data = request.get_json(silent=True) or {}
            key = data.get("LicenseKey")
            machine = data.get("MachineId")

        print("📥 LicenseKey:", key)
        print("💻 MachineId:", machine)

        # ❌ VALIDATION
        if not key or not machine:
            return jsonify({
                "status": "invalid",
                "message": "LicenseKey / MachineId missing"
            })

        # 🔍 FETCH
        lic = get_license(key)

        if not lic:
            return jsonify({
                "status": "invalid",
                "message": "License not found"
            })

        # 👉 (id, key, machine_id, is_used, expiry_date)
        _, license_key, db_machine, is_used, expiry = lic

        # =================================================
        # ⏳ EXPIRY CHECK
        # =================================================
        if expiry:
            try:
                expiry_date = datetime.strptime(expiry, "%Y-%m-%d")

                if datetime.now() > expiry_date:
                    return jsonify({
                        "status": "expired",
                        "message": "License expired"
                    })

            except Exception as e:
                print("⚠️ Expiry parse error:", str(e))

        # =================================================
        # 🟢 FIRST ACTIVATION
        # =================================================
        if not is_used:
            update_license(machine, key)

            return jsonify({
                "status": "activated",
                "message": "License activated successfully"
            })

        # =================================================
        # 🔁 SAME MACHINE
        # =================================================
        if db_machine == machine:
            return jsonify({
                "status": "already_activated",
                "message": "Already activated on this machine"
            })

        # =================================================
        # ❌ OTHER MACHINE BLOCK
        # =================================================
        return jsonify({
            "status": "used_in_other_pc",
            "message": "License already used on another device"
        })

    except Exception as e:
        print("❌ ACTIVATE ERROR:", str(e))

        return jsonify({
            "status": "error",
            "message": str(e)
        })


# =========================================================
# 🔥 GENERATE LICENSE (ADMIN)
# =========================================================
@license_bp.route("/generate", methods=["GET", "POST"])
def generate():
    try:
        data = request.get_json(silent=True) or {}

        days = int(data.get("days", 30))

        # 🔑 UNIQUE KEY
        key = "DSAI-" + str(uuid.uuid4())[:8].upper()

        expiry = (datetime.now() + timedelta(days=days)).strftime("%Y-%m-%d")

        print("🆕 Generating License:", key)

        create_license(key, expiry)

        return jsonify({
            "status": "created",
            "key": key,
            "expiry": expiry
        })

    except Exception as e:
        print("❌ GENERATE ERROR:", str(e))

        return jsonify({
            "status": "error",
            "message": str(e)
        })