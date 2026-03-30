import requests
import json
import os
from core.machine import get_machine_id

LICENSE_FILE = "storage/license.json"
API_URL = "https://diffsenseai-ai.onrender.com/api/license/activate"
TIMEOUT = 10


def is_activated():
    return os.path.exists(LICENSE_FILE)


def save_license(data):
    os.makedirs("storage", exist_ok=True)
    with open(LICENSE_FILE, "w") as f:
        json.dump(data, f)


def load_license():
    try:
        with open(LICENSE_FILE) as f:
            return json.load(f)
    except:
        return None


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

        data = res.json()

    except requests.exceptions.Timeout:
        return "timeout"

    except requests.exceptions.ConnectionError:
        return "no_server"

    except Exception as e:
        return f"error:{str(e)}"

    status = data.get("status", "").lower()

    if status in ["activated", "already_activated"]:
        save_license({
            "key": key,
            "machine": machine
        })
        return "success"

    if status == "invalid":
        return "invalid"

    if status == "used_in_other_pc":
        return "used"

    return "unknown"


def validate_local():
    if not is_activated():
        return False

    data = load_license()

    if not data:
        return False

    if data.get("machine") != get_machine_id():
        return False

    return True