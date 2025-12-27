
import os
from dotenv import load_dotenv
load_dotenv()
from app.core.security import get_username
import pytest
from app.schemas.user_schemas import UserCreation
from ..config import get_client,get_engine,get_session
from ..utils.user_crud import create_test_user

def test_login(get_client, get_session):
    create_test_user(
        get_session,
        username="alpha_45",
        password="Qwerty123",
    )

    resp = get_client.post(
        "/auth/login",
        data={
            "username": "alpha_45",
            "password": "Qwerty123",
        },
    )
    
    assert resp.status_code == 200

    body = resp.json()
    assert "access_token" in body

    decoded_username = get_username(body["access_token"])
    assert decoded_username == "alpha_45"
    


def test_signup(get_session,get_client):
    
    usercreate=UserCreation(email_id="oicoi@email.com",username="alpha_45",password="Qwerty123")
    resp = get_client.post(
        "/auth/signup",
        json=usercreate.model_dump()
    )
    assert resp.status_code==200
    body=resp.json()

    assert "id" in body
    assert "username" in body
    assert body["username"]=="alpha_45"


    