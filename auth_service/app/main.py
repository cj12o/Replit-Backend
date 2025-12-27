from fastapi import FastAPI
from  contextlib import asynccontextmanager
from dotenv import load_dotenv
load_dotenv()
from app.db.session import create_db_and_tables

from app.api.v1.auth import router as auth_router
from app.api.v1.users import router as user_router


@asynccontextmanager
async def lifespan(app:FastAPI):
   create_db_and_tables()
   yield




app=FastAPI(lifespan=lifespan)
app.include_router(auth_router)
app.include_router(user_router)



