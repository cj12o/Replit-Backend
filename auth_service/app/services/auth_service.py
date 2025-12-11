from typing import Annotated
from fastapi import Depends
from app.core.security import decodeJwtToken
from fastapi import HTTPException,status
from jwt.exceptions import InvalidTokenError
from app.schemas.token import TokenData
from sqlmodel import select,Session
from app.db.models import User
from app.db.database import getSession
from fastapi.security import OAuth2PasswordBearer
from app.core.security import verifyPassword

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

def get_user(username:str,session:Session):
    "retrives user from db"
    try:
        user=session.exec(select(User).where(User.username==username)).first()
        if not user:
            raise credentials_exception
        return user
    except InvalidTokenError:
        raise credentials_exception
    



def get_current_user(token:Annotated[str,Depends(oauth2_scheme)],session:Annotated[Session,Depends(getSession)]):
    try:
        payload=decodeJwtToken(token)
        print(f"✅✅Payload:{payload}")
        if payload is None:
            raise credentials_exception
        username=payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data=TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    user=get_user(username,session)
    if not user:
        raise credentials_exception
    return user


def get_current_active_user(user:Annotated[User,Depends(get_current_user)]):
    if not user.active:
        raise HTTPException(
            status_code=400,
            detail="Inactive user"
        )
    return user