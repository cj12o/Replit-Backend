from fastapi import FastAPI,WebSocket
from .core.teminal import run_in_terminal
from .schema.ws_schema import websocket_Request,websocket_Response
import json

app=FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.websocket("/ws")
async def ws_endpoint(ws:WebSocket):
    await ws.accept()
    while True:
        json_obj=await ws.receive_json()
        instance=websocket_Request.model_validate(json_obj)
        if not instance.is_cmd:
            return websocket_Response().model_dump()
       
        #execute
        if instance.user_cmd:
            error_occured,result=run_in_terminal(instance.user_cmd)
            if result:
                if error_occured:
                    resp_obj=websocket_Response(
                        is_cmd_output=True,
                        user_cmd=instance.user_cmd,
                        error_msg=str(result)
                    )
                else:
                    resp_obj=websocket_Response(
                        is_cmd_output=True,
                        user_cmd=instance.user_cmd,
                        cmd_output=str(result)
                    )

                await ws.send_json(resp_obj.model_dump())
            
        await ws.send_json(websocket_Response().model_dump())

   