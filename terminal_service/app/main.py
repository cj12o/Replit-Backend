from fastapi import FastAPI,WebSocket


app=FastAPI()


@app.get("/jhvuy")
async def root():
    return {"message": "Hello World"}


@app.websocket("/ws")
async def ws_endpoint(ws:WebSocket):
    await ws.accept()
    while True:
        data=await ws.receive_text()
        await ws.send_text(data)

   