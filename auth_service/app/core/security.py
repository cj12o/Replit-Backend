#this file :
# handles hashing and jwt encoding + decoding

from passlib.hash import pbkdf2_sha256
from jose import jwt,JWTError
from datetime import timedelta,datetime,timezone
from typing import Any


SECRET_KEY="123"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def verifyPassword(orginal_pass:str,hashed_pass:str)->bool:
    "verify hashed password" 
    return pbkdf2_sha256.verify(orginal_pass,hashed_pass)


def getHashedPassword(orginal_pass:str)->str:
    "returns hashed password"
    return pbkdf2_sha256.hash(orginal_pass)


def createJwtToken(data:dict,expires_delta=timedelta|None=None)->str:
    try:
        data_to_encode=data.copy()
        # if expires_delta is not None:
        #     expire=datetime.now(timezone.utc) + expires_delta
        # else:
        expire=datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        data_to_encode.update({"expire":expire,"sub":str(data.get("user_id"))})
        encoded_jwt=jwt.encode(data_to_encode,SECRET_KEY,ALGORITHM)
        return encoded_jwt
    except Exception  as e:
        print(f"Error in creating JWT token:{str(e)}")
        return None

def decodeJwtToken(token:str):
    try:
        decoded_jwt=jwt.decode(token,SECRET_KEY,[ALGORITHM])
        return decodeJwtToken
    except JWTError as je:
        print(f"Error in decoding JWT token:{str(je)}")
        return None
    
