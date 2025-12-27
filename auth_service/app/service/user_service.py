from ..db.session import sessionDep
from  ..schemas.user_schemas import UserCreation
from ..models.user_model import User
from sqlmodel import select
from fastapi import HTTPException,status
from ..core.security import get_hashed_password
from fastapi import HTTPException


async def get_user_by_email(sesh:sessionDep,email_id:str):
    user=sesh.exec(select(User).where(email_id==User.email_id)).first()
    return user

async def get_user_by_username(sesh:sessionDep,username:str):
    user=sesh.exec(select(User).where(username==User.username)).first()
    return user

async def get_user_by_userid(sesh:sessionDep,userid:int):
    user=sesh.exec(select(User).where(User.id==userid)).first()
    return user

async def create_user(sesh:sessionDep,user_data:UserCreation):
    hashed_pass=get_hashed_password(user_data.password)
    user=User(username=user_data.username,
        hashed_password=hashed_pass,
        email_id=user_data.email_id,
        is_active=user_data.is_active,
        is_super_user=user_data.is_super_user)
    
    sesh.add(user)
    sesh.commit()
    sesh.refresh(user)
    return user


async def delete_user_by_id(sesh:sessionDep,user_id:int):
    user=await get_user_by_userid(sesh,user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    sesh.delete(user)
    sesh.commit()
     
    
