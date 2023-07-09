from ..connmanager import ConnectionManager
from ..encryption import generate_key

class Rooms:
    def __init__(self):
        self.rooms: dict[str, Room] = {}

    def create_room(self, room_code: str):
        self.rooms[room_code] = Room(room_code)
        return self.rooms[room_code]

    def find_room(self, room_code: str):
        room = self.rooms.get(room_code)

        if not room:
            room = self.create_room(room_code)
        
        return room

    def find_connection_room(self, ws):
        for room in self.rooms.values():
            if room.connections.has_connection(ws):
                return room

class Room:
    def __init__(self, room_code: str):
        self.room_code = room_code
        self.connections = ConnectionManager()
        self.secret_key = generate_key()