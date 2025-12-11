from fastapi import Depends,HTTPException
from sqlmodel import Field,Session,SQLModel,table,create_engine
from .database import engine
from typing import Annotated

class User(SQLModel,table=True):
    id:int|None=Field(default=None,primary_key=True)
    username:str=Field(default=str,unique=True,index=True)
    password:str=Field(default=str)
    active:bool=Field(default=False)


class create_db_and_tables():
    SQLModel.metadata.create_all(engine)


