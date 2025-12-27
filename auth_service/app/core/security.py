from pwdlib import PasswordHash
from datetime import timedelta,datetime,timezone
import jwt
import os
from fastapi import HTTPException,status
from jose import JWTError

SECRET_KEY = str(os.getenv("SECRET_KEY"))
ALGORITHM = str(os.getenv("ALGORITHM"))
ACCESS_TOKEN_EXPIRE_MINUTES = float(str(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")))

password_hash=PasswordHash.recommended()


def get_hashed_password(password:str)->str:
    return password_hash.hash(password)

def verify_password(plain_password:str,hashed_password:str):
    return password_hash.verify(plain_password,hashed_password)


def create_access_token(sub:str,expires_delta:timedelta|None=None):
    "returns a JWT"

    if expires_delta is not None:
        expiry=datetime.now(timezone.utc) + expires_delta
    else:
        expiry=datetime.now(timezone.utc)+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode={"sub":sub,"exp":int(expiry.timestamp())} #note :exp ,not any other name as exp gets automatically enforced by libs
    encoded_jwt=jwt.encode(payload=to_encode,key=SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt
    

def get_username(token:str):
    "returns a username by decoding jwt"
    try:
        payload=jwt.decode(jwt=token,key=SECRET_KEY,algorithms=ALGORITHM)
        username=payload.get("sub")
        return username
    except jwt.exceptions.DecodeError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )
