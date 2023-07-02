import tkinter as tk
from tkinter import messagebox
import customtkinter
import asyncio
import json
import webbrowser
from .app import App
from .settings import Settings
from ..comm import server
from ..utils.nickname import check_nickname
from ..config import read_config

class RoomPicker(customtkinter.CTk):
    def __init__(self, loop: asyncio.AbstractEventLoop):
        self.loop = loop
        self.room_code = None
        loop.run_until_complete(server.connect())
        customtkinter.set_appearance_mode("System")
        customtkinter.set_default_color_theme("blue")

        super().__init__()

        self.title("SCH - Room Picker")
        self.geometry("350x170")
        self.resizable(False, False)
        self.iconbitmap(read_config()["client"]["icon_path"])

        self.room_number_frame = customtkinter.CTkFrame(self, width=300, height=100, corner_radius=10)
        self.room_number_input = customtkinter.CTkEntry(self.room_number_frame, width=285, height=45, corner_radius=10, placeholder_text="Type the room code here...")
        self.room_submit_btn = customtkinter.CTkButton(self.room_number_frame, text="Join", width=60, height=40, corner_radius=10,
                                                       command=lambda: loop.run_until_complete(self.submit_callback()))

        self.bind("<Return>", lambda _: loop.run_until_complete(self.submit_callback()))

        self.room_submit_btn.pack(side=tk.RIGHT, padx=5)
        self.room_number_input.pack(padx=10, pady=10)
        self.room_number_frame.pack(padx=20, pady=20)

        self.additional_buttons_frame = customtkinter.CTkFrame(self, width=300, height=50, corner_radius=10, fg_color="transparent")

        self.settings_btn = customtkinter.CTkButton(self.additional_buttons_frame, text="Settings", width=60, height=40, corner_radius=10,
                                                    command=self.settings_callback)
        self.settings_btn.grid(row=0, column=0, padx=5)

        self.settings_btn = customtkinter.CTkButton(self.additional_buttons_frame, text="About", width=60, height=40, corner_radius=10,
                                                    command=self.about_callback)
        self.settings_btn.grid(row=0, column=1, padx=5)

        self.additional_buttons_frame.pack()

        self.settings = None
        self.about = None

    async def submit_callback(self):
        if not self.room_number_input.get():
            return

        try:
            self.room_code = self.room_number_input.get()
            self.destroy()

            nickname = read_config()["client"].get("nickname")
            check, reason = check_nickname(nickname)
            if not check:
                nickname = None
                messagebox.showwarning("Warning", reason)

            await asyncio.sleep(1)
            await server.server.send(json.dumps({
                "type": "room_join",
                "room_code": self.room_code,
                "nickname": nickname
            }))

            self.open_app()
        except Exception:
            await server.connect()
            await server.server.send(json.dumps({
                "type": "room_join",
                "room_code": self.room_code,
                "nickname": nickname
            }))

            self.open_app()
    
    def destroy(self):
        super().destroy()

    def open_app(self):
        app = App(self.loop, self.room_code)
        app.mainloop()

    def settings_callback(self):
        if self.settings is None or not self.settings.winfo_exists():
            self.settings = Settings(self)
            self.after(150, lambda: self.settings.focus())
        else:
            self.settings.reload_config()
            self.settings.focus()

    def about_callback(self):
        webbrowser.open("https://github.com/nawafalqari/sch")
        # if self.about is None or not self.about.winfo_exists():
        #     self.about = About(self)
        #     self.after(150, lambda: self.about.focus())
        # else:
        #     self.about.focus()
            