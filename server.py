import uvicorn
from server import create_app

uvicorn.run(create_app(), port=5555)