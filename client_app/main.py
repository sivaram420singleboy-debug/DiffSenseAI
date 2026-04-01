import os
import sys

def get_base_path():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.abspath(os.path.dirname(__file__))

BASE_PATH = get_base_path()
LICENSE_FILE = os.path.join(BASE_PATH, "license.txt")

sys.path.insert(0, BASE_PATH)

from ui.main_screen import open_main_app
from ui.license_screen import open_license_screen


def is_activated():
    return os.path.exists(LICENSE_FILE)


def main():
    if is_activated():
        print("✅ License Found → Opening Main")
        open_main_app()
    else:
        print("🔐 No License → Opening License Screen")
        open_license_screen(open_main_app)


if __name__ == "__main__":
    main()