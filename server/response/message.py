from .resp import Response

class Message(Response):
    def __init__(self, connection, message: str, whisper: bool = False):
        if whisper:
            self.content = f"{connection.nickname} Whispered: {message}"
        else:
            self.content = f"{connection.nickname}: {message}"

        self.data = {
            "content": self.content,
            "whisper": whisper,
        }