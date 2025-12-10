from dotenv import load_dotenv
from fastapi import Depends
from sqlmodel import Session
from sqlmodel import SQLModel,create_engine
import os
from typing import Annotated

from dotenv import load_dotenv
load_dotenv()

db_url=str(os.getenv("DB_CONN_URL",""))
engine=create_engine(url=db_url)


def getSession():
    with Session(engine) as sesh:
        yield sesh

sessionDep=Annotated[Session,Depends(getSession)]