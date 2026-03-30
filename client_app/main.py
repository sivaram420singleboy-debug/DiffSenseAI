import sys
import os

# 👉 EXE + normal run compatible path
def get_base_path():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.abspath(os.path.dirname(__file__))


BASE_PATH = get_base_path()

# 👉 core import fix
sys.path.append(os.path.abspath(os.path.join(BASE_PATH, '..')))

from core.license_manager import validate_local
from ui.license_screen import open_license_screen
from ui.main_screen import open_main_app


def main():
    try:
        if validate_local():
            print("✅ License valid → Opening Main App")
            open_main_app()
        else:
            print("🔑 License not found → Opening License Screen")
            open_license_screen(open_main_app)

    except Exception as e:
        print("❌ App Error:", str(e))


if __name__ == "__main__":
    main()