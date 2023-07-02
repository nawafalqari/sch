import websockets.client
import websockets.exceptions
from tkinter import messagebox, Tk
from ..config import read_config

class Server:
    def __init__(self):
        self.host = read_config()["server"]["host"]

    async def connect(self):
        try:
            self.server = await websockets.client.connect(self.host)
        except ConnectionRefusedError:
            messagebox.showerror(title="Error", message=f"Error connecting to server: {self.host}\nupdate the host in the settings menu")