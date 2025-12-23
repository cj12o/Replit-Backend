import pydantic  
from pydantic import BaseModel,Field
from typing import Annotated,Optional

class websocket_Response(BaseModel):
    is_cmd_output:bool=Field(default=False,description="if its a command output")
    user_cmd:Optional[str]=Field(default=None,description="the command sent by user")
    cmd_output:Optional[str]=Field(default=None,description="the output of the command")
    generic_msg:Optional[str]=Field(default=None,description="generic message")
    error_msg:Optional[str]=Field(default=None,description="error message")


class websocket_Request(BaseModel):
    user_cmd:Optional[str]=Field(description="the command sent by user")
    is_cmd:Optional[bool]=Field(default=False,description="if its a command output")

