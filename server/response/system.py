from .resp import Response

class System(Response):
    def __init__(self, message: str):
        self.data = {
            "content": f"System> {message}"
        }

class SystemAction(Response):
    def __init__(self, action: str, after_message: str = None, **kwargs):
        self.data = {
            "type": "system.action",
            "action": action,
            "after_message": after_message,
            **kwargs
        }