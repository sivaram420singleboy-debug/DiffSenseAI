import customtkinter as ctk

def open_main_app():

    app = ctk.CTk()
    app.geometry("600x400")
    app.title("DiffSenseAI")

    frame = ctk.CTkFrame(app)
    frame.pack(expand=True, fill="both", padx=20, pady=20)

    ctk.CTkLabel(
        frame,
        text="🚀 DiffSense AI",
        font=("Arial", 26, "bold")
    ).pack(pady=20)

    ctk.CTkLabel(
        frame,
        text="License Activated Successfully ✅",
        font=("Arial", 14)
    ).pack(pady=10)

    # 🔥 Future buttons
    ctk.CTkButton(frame, text="📂 Compare Files").pack(pady=10)
    ctk.CTkButton(frame, text="🧠 AI Tools").pack(pady=10)
    ctk.CTkButton(frame, text="📊 Reports").pack(pady=10)

    app.mainloop()