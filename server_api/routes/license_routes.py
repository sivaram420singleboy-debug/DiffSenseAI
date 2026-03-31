from flask import Blueprint, request, jsonify
from server_api.models.license_model import get_license, update_license, create_license
import os
import uuid
from datetime import datetime, timedelta

license_bp = Blueprint("license", __name__)

print("🔥 USING DB:", os.path.abspath("server_api/database/db.sqlite3"))


# =========================================================
# 🔑 ACTIVATE LICENSE (FINAL FIXED)
# =========================================================
@license_bp.route("/activate", methods=["GET", "POST"])
def activate():
    try:
        # =================================================
        # 🔥 GET / POST SUPPORT
        # =================================================
        if request.method == "GET":
            key = request.args.get("LicenseKey")
            machine = request.args.get("MachineId")
        else:
            data = request.get_json(silent=True) or {}

            print("📥 FULL JSON:", data)   # 🔥 DEBUG

            # 🔥 SUPPORT BOTH KEY FORMATS (VERY IMPORTANT)
            key = data.get("LicenseKey") or data.get("license_key")
            machine = data.get("MachineId") or data.get("machine_id")

        print("🔑 KEY:", key)
        print("💻 MACHINE:", machine)

        # =================================================
        # ❌ VALIDATION
        # =================================================
        if not key or not machine:
            return jsonify({
                "status": "invalid",
                "message": "LicenseKey / MachineId missing"
            })

        lic = get_license(key)

        print("🔎 DB RESULT:", lic)  # 🔥 DEBUG

        if not lic:
            return jsonify({
                "status": "invalid",
                "message": "License not found"
            })

        # 👉 SAFE UNPACK (handle both 4/5 columns)
        if len(lic) == 5:
            _, license_key, db_machine, is_used, expiry = lic
        else:
            _, license_key, db_machine, is_used = lic
            expiry = None

        print("📊 DB MACHINE:", db_machine)
        print("📊 IS USED:", is_used)
        print("📊 EXPIRY:", expiry)

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
            print("🟢 FIRST TIME ACTIVATION")

            update_license(machine, key)

            return jsonify({
                "status": "activated",
                "message": "License activated successfully"
            })

        # =================================================
        # 🔁 SAME PC
        # =================================================
        if db_machine == machine:
            print("🔁 SAME MACHINE")

            return jsonify({
                "status": "already_activated",
                "message": "Already activated on this machine"
            })

        # =================================================
        # ❌ OTHER PC
        # =================================================
        print("❌ USED IN OTHER PC")

        return jsonify({
            "status": "used_in_other_pc",
            "message": "License already used on another device"
        })

    except Exception as e:
        print("❌ ERROR:", str(e))

        return jsonify({
            "status": "error",
            "message": str(e)
        })


# =========================================================
# 🔥 GENERATE LICENSE (ADMIN)
# =========================================================
@license_bp.route("/generate", methods=["POST"])
def generate():
    try:
        data = request.get_json(silent=True) or {}

        days = int(data.get("days", 30))

        key = "DSAI-" + str(uuid.uuid4())[:8].upper()
        expiry = (datetime.now() + timedelta(days=days)).strftime("%Y-%m-%d")

        create_license(key, expiry)

        return jsonify({
            "status": "created",
            "key": key,
            "expiry": expiry
        })

    except Exception as e:
        print("❌ ERROR:", str(e))

        return jsonify({
            "status": "error",
            "message": str(e)
        })