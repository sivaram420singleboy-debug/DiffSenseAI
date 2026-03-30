import customtkinter as ctk

ctk.set_appearance_mode("dark")

def open_main_app():
    app = ctk.CTk()
    app.geometry("600x400")
    app.title("DiffSenseAI - Dashboard")

    frame = ctk.CTkFrame(app)
    frame.pack(padx=20, pady=20, fill="both", expand=True)

    ctk.CTkLabel(
        frame,
        text="🚀 ImageGrafix",
        font=("Segoe UI", 24, "bold")
    ).pack(pady=20)

    ctk.CTkLabel(
        frame,
        text="License Activated Successfully ✅",
        font=("Segoe UI", 14)
    ).pack(pady=10)

    app.mainloop()