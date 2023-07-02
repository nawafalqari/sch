from fastapi import FastAPI, WebSocket
from ..connmanager import connection_handler

def create_app() -> FastAPI:
    app = FastAPI()

    @app.websocket("/ws")
    async def server(ws: WebSocket):
        await ws.accept()

        await connection_handler(ws)

    return app