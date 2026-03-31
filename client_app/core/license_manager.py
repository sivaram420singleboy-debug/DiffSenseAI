import requests
import json
import os
from core.machine import get_machine_id

LICENSE_FILE = "storage/license.json"
API_URL = "https://diffsenseai-ai.onrender.com/api/license/activate"
TIMEOUT = 10


# =========================================================
# ✅ CHECK LICENSE EXIST
# =========================================================
def is_activated():
    return os.path.exists(LICENSE_FILE)


# =========================================================
# 💾 SAVE LICENSE
# =========================================================
def save_license(data):
    os.makedirs("storage", exist_ok=True)
    with open(LICENSE_FILE, "w") as f:
        json.dump(data, f)
    print("💾 License saved locally")


# =========================================================
# 📂 LOAD LICENSE
# =========================================================
def load_license():
    try:
        with open(LICENSE_FILE) as f:
            return json.load(f)
    except:
        return None


# =========================================================
# 🔥 MAIN ACTIVATION FUNCTION (FINAL DEBUG VERSION)
# =========================================================
def activate_license(key):
    machine = get_machine_id()

    print("🔑 KEY:", key)
    print("💻 MACHINE ID:", machine)
    print("🌐 API:", API_URL)

    try:
        res = requests.post(
            API_URL,
            json={
                "LicenseKey": key,
                "MachineId": machine
            },
            timeout=TIMEOUT
        )

        # 🔥 DEBUG OUTPUT
        print("🌐 STATUS CODE:", res.status_code)
        print("🌐 RAW RESPONSE:", res.text)

        # 🔥 SAFE JSON PARSE
        try:
            data = res.json()
        except:
            print("❌ JSON PARSE FAILED")
            return "Invalid server response ❌"

    except requests.exceptions.Timeout:
        print("❌ TIMEOUT ERROR")
        return "Server Timeout ❌"

    except requests.exceptions.ConnectionError:
        print("❌ CONNECTION ERROR")
        return "Server Not Running ❌"

    except Exception as e:
        print("❌ UNKNOWN ERROR:", str(e))
        return f"Error ❌: {str(e)}"

    # =========================================================
    # 🔍 HANDLE RESPONSE
    # =========================================================
    status = data.get("status") or data.get("message")

    if not status:
        print("❌ INVALID RESPONSE FORMAT:", data)
        return "Invalid response ❌"

    status = str(status).lower()
    print("🔍 FINAL STATUS:", status)

    # =========================================================
    # ✅ SUCCESS
    # =========================================================
    if status in ["activated", "already_activated"]:
        save_license({
            "key": key,
            "machine": machine
        })
        print("✅ ACTIVATION SUCCESS")
        return True

    # =========================================================
    # ❌ INVALID KEY
    # =========================================================
    if status == "invalid":
        print("❌ INVALID KEY")
        return "Invalid License ❌"

    # =========================================================
    # ❌ USED IN OTHER PC
    # =========================================================
    if status == "used_in_other_pc":
        print("❌ USED IN OTHER PC")
        return "Used in another PC ❌"

    # =========================================================
    # ❌ UNKNOWN
    # =========================================================
    print("❌ UNKNOWN STATUS:", status)
    return f"Unknown Error ❌ ({status})"


# =========================================================
# ✅ LOCAL VALIDATION (OFFLINE SUPPORT)
# =========================================================
def validate_local():
    if not is_activated():
        print("❌ No license file")
        return False

    data = load_license()

    if not data:
        print("❌ License file corrupted")
        return False

    if data.get("machine") != get_machine_id():
        print("❌ Machine mismatch")
        return False

    print("✅ Local validation success")
    return True