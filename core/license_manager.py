import requests
import json
import os
from core.machine import get_machine_id

LICENSE_FILE = "storage/license.json"

API_URL = "http://127.0.0.1:5000/api/license/activate"
TIMEOUT = 10


# ✅ Check license file exist
def is_activated():
    return os.path.exists(LICENSE_FILE)


# ✅ Save license locally
def save_license(data):
    os.makedirs("storage", exist_ok=True)
    with open(LICENSE_FILE, "w") as f:
        json.dump(data, f)


# ✅ Load local license
def load_license():
    try:
        with open(LICENSE_FILE) as f:
            return json.load(f)
    except:
        return None


# 🔥 MAIN ACTIVATION FUNCTION
def activate_license(key):
    machine = get_machine_id()

    try:
        res = requests.post(
            API_URL,
            json={
                "LicenseKey": key,
                "MachineId": machine
            },
            timeout=TIMEOUT
        )

        print("🌐 SERVER RESPONSE:", res.text)

        # 🔥 SAFE JSON PARSE
        try:
            data = res.json()
        except:
            return "Invalid server response ❌"

    except requests.exceptions.Timeout:
        return "Server Timeout ❌"

    except requests.exceptions.ConnectionError:
        return "Server Not Running ❌"

    except Exception as e:
        return f"Error ❌: {str(e)}"

    # 🔥 HANDLE BOTH status & message
    status = data.get("status") or data.get("message")

    if not status:
        return "Invalid response ❌"

    status = str(status).lower()

    # ✅ SUCCESS
    if status in ["activated", "already_activated"]:
        save_license({
            "key": key,
            "machine": machine
        })
        return True

    # ❌ INVALID KEY
    if status == "invalid":
        return "Invalid License ❌"

    # ❌ USED IN OTHER PC
    if status == "used_in_other_pc":
        return "Used in another PC ❌"

    return f"Unknown Error ❌ ({status})"


# ✅ LOCAL VALIDATION (OFFLINE SUPPORT)
def validate_local():
    if not is_activated():
        return False

    data = load_license()

    if not data:
        return False

    # 🔥 MACHINE LOCK
    if data.get("machine") != get_machine_id():
        return False

    return True