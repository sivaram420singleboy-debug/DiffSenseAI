import sys
import os

# 🔥 FIX PATH (EXE SUPPORT)
def get_base_path():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))


BASE_PATH = get_base_path()

# 👉 ADD CURRENT FOLDER TO PATH
sys.path.append(BASE_PATH)

# 👉 IMPORTS (NOW SAFE)
from core.license_manager import validate_local
from ui.license_screen import open_license_screen
from ui.main_screen import open_main_app


def main():
    try:
        if validate_local():
            print("✅ License OK → Main App")
            open_main_app()
        else:
            print("🔑 Open License Screen")
            open_license_screen(open_main_app)

    except Exception as e:
        print("❌ ERROR:", str(e))


if __name__ == "__main__":
    main()