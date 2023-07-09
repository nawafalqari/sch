import asyncio
import nest_asyncio
from client import RoomPicker

nest_asyncio.apply()

if __name__ == "__main__":
    event_loop = asyncio.get_event_loop()
    rp = RoomPicker(event_loop)
    rp.mainloop()