import uvicorn
import sys
import asyncio
import nest_asyncio
from server import create_app
from client import App, RoomPicker

nest_asyncio.apply()

if sys.argv[1] == "client":
    # App().mainloop()
    RoomPicker(asyncio.get_event_loop()).mainloop()
elif sys.argv[1] == "server":
    uvicorn.run(create_app(), port=5555)