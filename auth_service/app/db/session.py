from sqlmodel import create_engine,Session
from fastapi import Depends
import os
from sqlmodel import SQLModel
from sqlalchemy import Engine
from typing import Annotated,TypeAlias


DB_URL=str(os.getenv("DB_URL",""))


engine=create_engine(DB_URL)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
        
sessionDep:TypeAlias=Annotated[Session,Depends(get_session)]
