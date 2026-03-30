import customtkinter as ctk
from core.license_manager import activate_license


def open_license_screen(start_main_app):

    app = ctk.CTk()
    app.geometry("450x300")
    app.title("DiffSenseAI - License Activation")

    def activate():
        key = entry.get().strip()

        if not key:
            label.configure(text="❌ Enter license key", text_color="red")
            return

        label.configure(text="⏳ Activating...", text_color="yellow")
        app.update()

        result = activate_license(key)

        if result == "success":
            label.configure(text="✅ Activated Successfully", text_color="green")

            def go_main():
                app.destroy()
                start_main_app()

            app.after(800, go_main)

        elif result == "invalid":
            label.configure(text="❌ Invalid License", text_color="red")

        elif result == "used":
            label.configure(text="❌ Used in another PC", text_color="red")

        elif result == "timeout":
            label.configure(text="❌ Server Timeout", text_color="red")

        elif result == "no_server":
            label.configure(text="❌ Server Not Running", text_color="red")

        else:
            label.configure(text=f"❌ {result}", text_color="red")

    frame = ctk.CTkFrame(app)
    frame.pack(expand=True, fill="both", padx=20, pady=20)

    ctk.CTkLabel(frame, text="🔐 Activate License", font=("Arial", 20)).pack(pady=10)

    entry = ctk.CTkEntry(frame, width=300, placeholder_text="DSAI-XXXX")
    entry.pack(pady=10)

    ctk.CTkButton(frame, text="Activate", command=activate).pack(pady=10)

    label = ctk.CTkLabel(frame, text="")
    label.pack(pady=10)

    app.mainloop()