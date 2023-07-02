from fastapi import WebSocket, WebSocketDisconnect
from ..rooms import rooms
from ..response import Message, System
from ..cmd import commands

async def connection_handler(ws: WebSocket):
    try:
        while True:
            data = await ws.receive_json()

            print(f"Received: {data}")

            match data["type"]:
                case "room_join":
                    room_code: str = data["room_code"]
                    room = rooms.find_room(room_code)

                    await room.connections.connect(ws, data)
                case "message":
                    message_content = data["content"]
                    room_code = data["room_code"]
                    room = rooms.find_room(room_code)

                    if message_content.startswith("/"):
                        cmd = commands.find_command(message_content)

                        if not cmd:
                            sys_response = System(f"command not found: {message_content}")
                            await room.connections.send(ws, sys_response)
                        else:
                            await cmd.callback(room, room.connections.get_connection(ws), message_content)
                    else:
                        message = Message(room.connections.get_connection(ws), message_content)

                        await room.connections.broadcast(message)
                case _:
                    pass
    except WebSocketDisconnect as disconnect:
        room = rooms.find_connection_room(ws)

        if room:
            await room.connections.disconnect(ws)
            
        if disconnect.code == 1000:
            pass
        else:
            print(f"{ws.client.host} Disconnected, code: {disconnect.code} ({disconnect.reason})")