import websockets.client
import websockets.exceptions
from tkinter import messagebox, Tk
from ..config import read_config

class Server:
    def __init__(self):
        self.host = read_config()["server"]["host"]

    async def connect(self):
        self.host = read_config()["server"]["host"]
        try:
            self.server = await websockets.client.connect(self.host)
        except ConnectionRefusedError:
            messagebox.showerror(title="Error", message=f"Error connecting to server: {self.host}\nupdate the host in the settings menu")
        except websockets.exceptions.InvalidURI:
            messagebox.showerror(title="Error", message=f"Invalid host: {self.host}\nupdate the host in the settings menu")
        except websockets.exceptions.InvalidStatusCode as err:
            messagebox.showerror(title="Error", message=f"Invalid status code from server: {self.host} ({err.status_code})\nupdate the host in the settings menu")
        except websockets.exceptions.InvalidHandshake:
            messagebox.showerror(title="Error", message=f"Invalid handshake with server: {self.host}\nupdate the host in the settings menu")