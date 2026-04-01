from flask import Blueprint, request, jsonify
from server_api.models.license_model import get_license, update_license, create_license
import uuid
from datetime import datetime, timedelta

license_bp = Blueprint("license", __name__)

print("🔥 LICENSE ROUTES LOADED")


# =========================================================
# 🔑 ACTIVATE LICENSE (100% FIXED)
# =========================================================
@license_bp.route("/activate", methods=["POST"])
def activate():
    try:
        data = request.get_json(silent=True) or {}

        print("📥 REQUEST:", data)

        key = data.get("LicenseKey") or data.get("license_key")
        machine = data.get("MachineId") or data.get("machine_id")

        if not key or not machine:
            return jsonify({
                "status": "invalid",
                "message": "LicenseKey / MachineId missing"
            })

        key = key.strip()

        # 🔎 FETCH
        lic = get_license(key)

        print("📊 DB:", lic)

        if not lic:
            return jsonify({
                "status": "invalid",
                "message": "License not found"
            })

        # SAFE UNPACK
        id_, license_key, db_machine, is_used, expiry = lic

        # =================================================
        # ⏳ EXPIRY CHECK
        # =================================================
        if expiry:
            expiry_date = datetime.strptime(expiry, "%Y-%m-%d")

            if datetime.now() > expiry_date:
                return jsonify({
                    "status": "expired"
                })

        # =================================================
        # 🟢 FIRST ACTIVATION
        # =================================================
        if is_used == 0:
            print("🟢 FIRST ACTIVATION")

            success = update_license(machine, key)

            if success:
                return jsonify({
                    "status": "activated"
                })
            else:
                return jsonify({
                    "status": "error"
                })

        # =================================================
        # 🔁 SAME PC
        # =================================================
        if db_machine == machine:
            return jsonify({
                "status": "already_activated"
            })

        # =================================================
        # ❌ OTHER PC
        # =================================================
        return jsonify({
            "status": "used_in_other_pc"
        })

    except Exception as e:
        print("❌ ERROR:", str(e))
        return jsonify({"status": "error", "message": str(e)})


# =========================================================
# 🔥 GENERATE LICENSE (WORKING)
# =========================================================
@license_bp.route("/generate", methods=["POST"])
def generate():
    try:
        data = request.get_json(silent=True) or {}

        days = int(data.get("days", 30))

        key = "DSAI-" + str(uuid.uuid4())[:8].upper()
        expiry = (datetime.now() + timedelta(days=days)).strftime("%Y-%m-%d")

        result = create_license(key, expiry)

        if result.get("status") == "created":
            return jsonify({
                "status": "created",
                "key": key,
                "expiry": expiry
            })

        return jsonify({"status": "error"})

    except Exception as e:
        print("❌ GENERATE ERROR:", str(e))
        return jsonify({"status": "error"})