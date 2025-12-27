from sqlmodel import Field,SQLModel
from typing import Optional


class User(SQLModel,table=True):
    id:int|None=Field(default=None,primary_key=True)
    username:str=Field(default=str,index=True)
    hashed_password:str=Field(default=str)
    email_id:str=Field(default=str,unique=True,index=True)
    is_active:Optional[bool]=Field(default=False)
    is_super_user:Optional[bool]=Field(default=False)
    