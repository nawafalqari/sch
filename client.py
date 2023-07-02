import client
import asyncio
import nest_asyncio

nest_asyncio.apply()

event_loop = asyncio.get_event_loop()
app = client.RoomPicker(event_loop)
app.mainloop()