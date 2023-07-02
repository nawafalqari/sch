import tkinter as tk
import customtkinter
import json
import asyncio
import websockets.exceptions
import threading
from ..comm import server
from ..config import read_config

class App(customtkinter.CTk):
    def __init__(self, loop: asyncio.AbstractEventLoop, room_code: str):
        self.loop = loop
        self.room_code = room_code

        super().__init__()

        self.title("SCH - Client")
        self.geometry("380x480")
        self.resizable(False, False)
        self.iconbitmap(read_config()["client"]["icon_path"])
        # self.minsize(380, 480)
        # self.maxsize(380, 480)

        self.messages_frame = customtkinter.CTkScrollableFrame(self, width=350, height=370, corner_radius=10)
        self.messages_frame.pack(padx=10, pady=10, expand=True, fill=tk.BOTH)

        self.input_frame = customtkinter.CTkFrame(self, width=350, height=100, corner_radius=10, fg_color="transparent")

        self.msg_input = customtkinter.CTkEntry(self.input_frame, width=285, height=45, corner_radius=10, placeholder_text="Type your message here...")
        self.msg_input.pack(side=tk.LEFT)

        self.send_btn = customtkinter.CTkButton(self.input_frame, text="Send", width=60, height=45, corner_radius=10,
                                                command=lambda: loop.run_until_complete(self.send_callback()))
        self.send_btn.pack(side=tk.RIGHT, padx=5)
        self.input_frame.pack(padx=10, pady=10)

        self.bind("<Return>", lambda _: loop.run_until_complete(self.send_callback()))

        self.receiver_thread = threading.Thread(
            target=lambda: loop.run_until_complete(self.receive_messages()),
            daemon=True
        ) 
        self.receiver_thread.start()
    
    async def send_callback(self):
        text = self.msg_input.get()

        if not text or text.isspace() or text.replace(" ", "") == "/":
            return

        self.msg_input.delete(0, tk.END)

        await server.server.send(json.dumps({
            "type": "message",
            "content": text,
            "room_code": self.room_code
        }))

    async def receive_messages(self):
        try:
            while server.server.open:
                data = await server.server.recv()
                data: dict = json.loads(data)

                match data["type"]:
                    case "message":
                        msg_widget = customtkinter.CTkLabel(self.messages_frame, text=data["content"], wraplength=330,
                                                            text_color="lightblue" if data.get("whisper") else None)
                        msg_widget.pack(anchor=tk.W)

                        self.messages_frame._parent_canvas.yview("scroll", int(2500 / 6), "units")
                    case "system":
                        msg_widget = customtkinter.CTkLabel(self.messages_frame, text=data["content"], wraplength=330, text_color="lightblue")
                        msg_widget.pack(anchor=tk.W)

                        self.messages_frame._parent_canvas.yview("scroll", int(2500 / 6), "units")
                    case "system.action":
                        match data["action"]:
                            case _:
                                pass

                        if data.get("after_message"):
                            msg_widget = customtkinter.CTkLabel(self.messages_frame, text=data["after_message"], wraplength=330, text_color="lightblue")
                            msg_widget.pack(anchor=tk.W)

                            self.messages_frame._parent_canvas.yview("scroll", int(2500 / 6), "units")                            
                        
        except websockets.exceptions.ConnectionClosedOK:
            pass

    def destroy(self):
        super().destroy()
        
        self.loop.run_until_complete(server.server.close())
        self.loop.stop()