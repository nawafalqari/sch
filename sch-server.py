import uvicorn
from server import app

HOST = "localhost"
PORT = 5555

if __name__ == "__main__":
    uvicorn.run(app, host=HOST, port=PORT)