import tkinter as tk
import customtkinter
from ..config import read_config

class About(customtkinter.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)

        self.title("SCH - About")
        self.geometry("350x200")
        self.resizable(False, False)
        self.after(250, lambda: self.iconbitmap(read_config()['client']['icon_path']))

        self.buttons_frame = customtkinter.CTkFrame(self, width=300, height=100, corner_radius=10, fg_color="transparent")

        self.github_btn = customtkinter.CTkButton(self.buttons_frame, text="GitHub", width=60, height=40, corner_radius=10, command=lambda: ...)
        self.github_btn.pack(padx=5, pady=5)

        self.website_btn = customtkinter.CTkButton(self.buttons_frame, text="Website", width=60, height=40, corner_radius=10, command=lambda: ...)
        self.website_btn.pack(padx=5, pady=5)

        self.buttons_frame.pack()