from sqlmodel import Session,select
from  app.models.user_model import User
from app.core.security import get_hashed_password

def create_test_user(
    session:Session,
    username:str="abc",
    password: str = "Qwerty123",
    email: str = "quartile@125.com",
    is_active: bool = True,
):
    hashed_password=get_hashed_password(password)
    user=User(username=username,hashed_password=hashed_password,email_id=email,is_active=False)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


