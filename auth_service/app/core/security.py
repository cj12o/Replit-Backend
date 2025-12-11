#this file :
# handles hashing and jwt encoding + decoding

from pwdlib import PasswordHash
import jwt
from fastapi import Depends,HTTPException,status
from datetime import timedelta,datetime,timezone
from typing import Annotated
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY=os.getenv("SECRET_KEY")
ALGORITHM=os.getenv("ALGORITHM","")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES",15))

password_hash=PasswordHash.recommended()


def verifyPassword(orginal_pass:str,hashed_pass:str)->bool:
    "verify hashed password" 
    return password_hash.verify(orginal_pass,hashed_pass)


def getHashedPassword(orginal_pass:str)->str:
    "returns hashed password"
    return password_hash.hash(orginal_pass)


def createJwtToken(data:dict,expires_delta:timedelta|None=None)->str|None:
    "creates and returns JWT Token"
    try:
        data_to_encode=data.copy()
        if expires_delta is not None:
            expire=datetime.now(timezone.utc) + expires_delta
        else:
            expire=datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

        data_to_encode.update({"exp":expire})
        encoded_jwt=jwt.encode(data_to_encode,SECRET_KEY,ALGORITHM)
        return encoded_jwt
    except Exception as e:
        print(f"Error in creatJwtToken :{str(e)}")
        return None

def decodeJwtToken(token:str):
    "decodes JWT Token returns Payload"
    try:
        payload=jwt.decode(token,SECRET_KEY,[ALGORITHM])
        return payload
    except Exception as e:
        print(f"Error in decoding JWT token:{str(e)}")
        return None
    


