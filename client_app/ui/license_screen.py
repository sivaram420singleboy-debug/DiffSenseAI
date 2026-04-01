import customtkinter as ctk
import os
import sys

# ================================
# 📁 BASE PATH (EXE SAFE)
# ================================
def get_base_path():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.abspath(os.path.dirname(__file__))

BASE_PATH = get_base_path()

# 🔥 IMPORTANT → same folder save ஆகணும்
LICENSE_FILE = os.path.join(BASE_PATH, "license.txt")

# 🎨 UI Theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


# ================================
# 🔐 LICENSE SCREEN
# ================================
def open_license_screen(start_main_app):

    app = ctk.CTk()
    app.geometry("450x300")
    app.title("DiffSenseAI - License Activation")
    app.resizable(False, False)

    # ================================
    # 🔥 ACTIVATE FUNCTION
    # ================================
    def activate():
        key = entry.get().strip()

        print("🔑 KEY:", key)  # debug

        if not key:
            label.configure(text="❌ Enter license key", text_color="red")
            return

        if not key.startswith("DSAI-"):
            label.configure(text="❌ Invalid Format", text_color="red")
            return

        try:
            # ✅ SAVE LICENSE FILE
            with open(LICENSE_FILE, "w") as f:
                f.write(key)

            print("✅ Saved at:", LICENSE_FILE)

            # 🔥 VERIFY FILE CREATED
            if os.path.exists(LICENSE_FILE):
                label.configure(text="✅ Activated Successfully", text_color="green")

                def go_main():
                    print("🚀 Opening Main App")
                    app.destroy()
                    start_main_app()

                app.after(800, go_main)
            else:
                label.configure(text="❌ Save Failed", text_color="red")

        except Exception as e:
            label.configure(text=f"❌ Error: {str(e)}", text_color="red")

    # ================================
    # 🧱 UI
    # ================================
    frame = ctk.CTkFrame(app, corner_radius=15)
    frame.pack(pady=30, padx=20, fill="both", expand=True)

    title = ctk.CTkLabel(
        frame,
        text="🔐 Activate Your License",
        font=("Segoe UI", 20, "bold")
    )
    title.pack(pady=15)

    subtitle = ctk.CTkLabel(
        frame,
        text="Enter your license key to continue",
        font=("Segoe UI", 12)
    )
    subtitle.pack(pady=5)

    entry = ctk.CTkEntry(
        frame,
        width=300,
        height=40,
        placeholder_text="DSAI-XXXX-XXXX",
        font=("Segoe UI", 12)
    )
    entry.pack(pady=15)

    btn = ctk.CTkButton(
        frame,
        text="Activate",
        width=200,
        height=40,
        command=activate,
        font=("Segoe UI", 14, "bold")
    )
    btn.pack(pady=10)

    label = ctk.CTkLabel(frame, text="")
    label.pack(pady=10)

    app.mainloop()