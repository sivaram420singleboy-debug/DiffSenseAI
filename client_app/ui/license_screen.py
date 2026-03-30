import customtkinter as ctk
from core.license_manager import activate_license

# 🎨 Theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


def open_license_screen(start_main_app):

    # 👉 Main Window (global use for destroy)
    app = ctk.CTk()
    app.geometry("450x300")
    app.title("DiffSenseAI - License Activation")
    app.resizable(False, False)

    # 🔥 Activate function
    def activate():
        key = entry.get().strip()

        if not key:
            label.configure(text="❌ Enter license key", text_color="red")
            return

        label.configure(text="⏳ Activating...", text_color="yellow")
        app.update()

        try:
            result = activate_license(key)
        except Exception as e:
            label.configure(text=f"❌ Error: {str(e)}", text_color="red")
            return

        print("RESULT:", result)

        # ✅ SUCCESS CASE
        if result is True or result == "success":
            label.configure(text="✅ Activated Successfully", text_color="green")

            def go_main():
                app.destroy()          # 👉 close license window
                start_main_app()       # 👉 open main screen

            app.after(800, go_main)

        # ❌ FAIL CASES
        else:
            if result == "invalid":
                msg = "❌ Invalid License Key"
            elif result == "used_in_other_pc":
                msg = "❌ Already used in another PC"
            elif result == "Server Not Running":
                msg = "❌ Server Not Running"
            elif result == "Server Timeout":
                msg = "❌ Server Timeout"
            else:
                msg = f"❌ {result}"

            label.configure(text=msg, text_color="red")

    # 🧱 UI Layout
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

    label = ctk.CTkLabel(
        frame,
        text="",
        font=("Segoe UI", 12)
    )
    label.pack(pady=10)

    app.mainloop()