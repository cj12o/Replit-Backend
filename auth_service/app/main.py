from fastapi import FastAPI,APIRouter,HTTPException
from app.db.models import create_db_and_tables
from contextlib import asynccontextmanager

from app.api.endpoints.auth import router as auth_router

@asynccontextmanager
async def lifespan(app:FastAPI):
    try:
        create_db_and_tables()
        print("created tables")
        yield
    except Exception as e:
        print(f"Error {str(e)}")


app=FastAPI(lifespan=lifespan)


app.include_router(auth_router, prefix="/auth")
