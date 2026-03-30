from flask import Blueprint, request, jsonify
from models.license_model import get_license, update_license, create_license
import os
import uuid
from datetime import datetime, timedelta

license_bp = Blueprint("license", __name__)

print("🔥 USING DB:", os.path.abspath("database/db.sqlite3"))


# 🔑 ACTIVATE LICENSE (GET + POST SUPPORT)
@license_bp.route("/activate", methods=["GET", "POST"])
def activate():
    try:
        # 🔥 SUPPORT BOTH (Installer → GET, App → POST)
        if request.method == "GET":
            key = request.args.get("LicenseKey")
            machine = request.args.get("MachineId")
        else:
            data = request.json
            key = data.get("LicenseKey")
            machine = data.get("MachineId")

        print("📥 Key:", key)
        print("💻 Machine:", machine)

        # ❌ VALIDATION
        if not key or not machine:
            return jsonify({"status": "invalid"})

        lic = get_license(key)

        if not lic:
            return jsonify({"status": "invalid"})

        # 👉 (id, key, machine_id, is_used, expiry)
        _, license_key, db_machine, is_used, expiry = lic

        # 🔥 EXPIRY CHECK
        if expiry:
            try:
                expiry_date = datetime.strptime(expiry, "%Y-%m-%d")
                if datetime.now() > expiry_date:
                    return jsonify({"status": "expired"})
            except:
                pass

        # 🔥 FIRST ACTIVATION
        if not is_used:
            update_license(machine, key)
            return jsonify({"status": "activated"})

        # 🔁 SAME PC
        if db_machine == machine:
            return jsonify({"status": "already_activated"})

        # ❌ OTHER PC
        return jsonify({"status": "used_in_other_pc"})

    except Exception as e:
        print("❌ ERROR:", str(e))
        return jsonify({"status": "error"})


# 🔥 GENERATE LICENSE (ADMIN)
@license_bp.route("/generate", methods=["POST"])
def generate():
    try:
        data = request.json

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
        return jsonify({"status": "error"})