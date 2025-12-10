from fastapi import Depends,HTTPException
from sqlmodel import Field,Session,SQLModel,table,create_engine
from .database import engine
from typing import Annotated

class User(SQLModel,table=True):
    id:int|None=Field(default=None,primary_key=True)
    email_id:str=Field(default=str,index=True,unique=True)
    password:str=Field(default=str,index=True)



class create_db_and_tables():
    SQLModel.metadata.create_all(engine)


