# test database

# DB isolation

# FastAPI dependency override

# TestClient
import pytest
from sqlmodel import create_engine,SQLModel,Session
from app.main import app
from typing import Annotated,TypeAlias
from fastapi import Depends,testclient
from app.db.session import get_session as app_get_session
from dependency_injector import containers,providers

@pytest.fixture
def get_engine():
    db_url="postgresql://postgres:1234@localhost:5432/replit_test_db"
    engine=create_engine(db_url)
    SQLModel.metadata.create_all(engine)
    yield engine
    SQLModel.metadata.drop_all(engine)

@pytest.fixture
def get_session(get_engine):
    with Session(get_engine) as session:
        yield session

@pytest.fixture
def get_client(get_session):
    def override_get_session():
        yield get_session

    app.dependency_overrides[app_get_session]=override_get_session

    with testclient.TestClient(app) as cl:
        yield cl
    
    app.dependency_overrides.clear()


