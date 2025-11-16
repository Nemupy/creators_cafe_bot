from threading import Thread
from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/")
async def root_get():
    return {"message": "Server is Online."}

@app.head("/")
async def root_head():
    return {"message": "Server is Online."}

def start():
    uvicorn.run(app, host="0.0.0.0", port=8080)

def server_thread():
    t = Thread(target=start)
    t.start()
