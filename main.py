import customtkinter as ctk
from app import ImageConverterApp

if __name__ == "__main__":
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")
    app = ImageConverterApp()
    app.run()
