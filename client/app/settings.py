import tkinter as tk
from tkinter import messagebox
import customtkinter
from ..config import read_config, update_config
from ..utils.nickname import check_nickname

class Settings(customtkinter.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)

        self.config = read_config()

        self.title(f"SCH - Settings ({self.config['server']['version']})")
        self.geometry("300x280")
        self.resizable(False, False)
        self.after(250, lambda: self.iconbitmap(self.config['client']['icon_path']))

        self.settings_frame = customtkinter.CTkFrame(self, width=300, height=150, corner_radius=10, fg_color="transparent")

        self.host_input = customtkinter.CTkEntry(self.settings_frame, width=200, height=40, corner_radius=10, placeholder_text="Host:")
        self.host_input.insert(0, self.config["server"]["host"])
        self.host_input.pack(pady=5)

        self.nickname_input = customtkinter.CTkEntry(self.settings_frame, width=200, height=40, corner_radius=10, placeholder_text="Nickname:")        
        if self.config["client"].get("nickname"):
            self.nickname_input.insert(0, self.config["client"]["nickname"])
        self.nickname_input.pack(pady=5)

        self.theme_select = customtkinter.CTkOptionMenu(self.settings_frame, width=200, height=40, corner_radius=10, values=["SCH", "Blue"], command=self.update_theme)
        self.theme_select.set(self.config["client"]["theme"])
        self.theme_select.pack(pady=5)

        self.notifications_checkbox = customtkinter.CTkCheckBox(self.settings_frame, text="Receive notifications", onvalue="True", offvalue="False")
        if read_config()["client"]["notifications"] == "True":
            self.notifications_checkbox.select()
        self.notifications_checkbox.pack(pady=5)

        self.options_frame = customtkinter.CTkFrame(self.settings_frame, width=300, height=100, corner_radius=10, fg_color="transparent")

        self.cancel_btn = customtkinter.CTkButton(self.options_frame, text="Cancel", width=60, height=40, corner_radius=10, fg_color="transparent", text_color="white", hover_color="black",  border_width=2, command=self.destroy)
        self.cancel_btn.grid(row=0, column=0, padx=5)

        self.save_btn = customtkinter.CTkButton(self.options_frame, text="Save", width=60, height=40, corner_radius=10, command=self.save_callback)
        self.save_btn.grid(row=0, column=1, padx=5)

        self.options_frame.pack(pady=5)
        self.settings_frame.pack(padx=20, pady=20)

    def save_callback(self):
        if len(self.host_input.get()) == 0:
            messagebox.showerror("Error", "Host must not be empty!")
            return

        check, reason = check_nickname(self.nickname_input.get())
        if not check:
            messagebox.showerror("Error", reason)
            return

        update_config(server={
                "host": self.host_input.get()
            },
            client={
                "theme": self.theme_select.get(),
                "nickname": self.nickname_input.get() if self.nickname_input.get() else "",
                "notifications": self.notifications_checkbox.get()
        })

        self.destroy()

    def update_theme(self, choice):
        if choice == "SCH":
            customtkinter.set_default_color_theme("sch-theme.json")
        elif choice == "Blue":
            customtkinter.set_default_color_theme("blue")
    
    def reload_config(self):
        self.config = read_config()