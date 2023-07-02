from fastapi import WebSocket
from ..response import Message, System, Response
from ..utils.nickname import check_nickname

# TODO: fix same nickname bug
# when two users connect then 1 leaves and rejoins the nickname will be the same for both users
# also when a user uses /nick he can use the same nickname as another user

class ConnectionManager:
    def __init__(self):
        self.connections: list[Connection] = []

    async def connect(self, ws: WebSocket, data: dict):
        nickname = self._assign_nickname(data.get("nickname"))

        conn = Connection(ws, nickname)

        self.connections.append(conn)
        await self.broadcast(System(f"{nickname} joined the room."))

    async def disconnect(self, ws: WebSocket):
        conn = self.get_connection(ws)

        self.connections.remove(conn)
        await self.broadcast(System(f"{conn.nickname} left the room."))

    async def broadcast(self, response: Response):
        for connection in self.connections:
            await connection.send(response)

    async def send(self, ws: WebSocket, response: Response):
        await self.get_connection(ws).send(response)

    def get_connection(self, ws: WebSocket):
        for conn in self.connections:
            if conn.ws == ws:
                return conn

    def get_connection_by_nickname(self, nickname: str):
        for conn in self.connections:
            if conn.nickname.lower() == nickname.lower():
                return conn
            
    def has_connection(self, ws: WebSocket):
        return self.get_connection(ws) is not None

    def _assign_nickname(self, nickname: str, n: int = 1):
        final_nickname = f"user{len(self.connections) + n}"

        if nickname and check_nickname(nickname)[0]:
            return nickname
        elif self.get_connection_by_nickname(final_nickname):
            return self._assign_nickname(None, n + 1)

        return final_nickname

class Connection:
    def __init__(self, ws: WebSocket, nickname: str = None):
        self.ws = ws
        self.nickname = nickname

    async def send(self, response: Response):
        await self.ws.send_json(response.to_dict())

    def __str__(self):
        return f"Connection({self.nickname})"