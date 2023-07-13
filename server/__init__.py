from .websocket import create_app

app = create_app(version="1.0.0-beta4", title="SCH - Server", description="Server for SCH (Secure Chat) application", docs_url=None, redoc_url=None)