from fastapi import APIRouter,status
from ...schemas.user_schemas import UserCreation,UserResponse
from ...db.session import sessionDep
from app.service.user_service import create_user,get_user_by_username,get_user_by_email
from  fastapi import HTTPException,Depends
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from app.core.security import verify_password,create_access_token
from app.errors import error_types

router=APIRouter(prefix="/auth")


@router.post("/signup",response_model=UserResponse)
async def signup(user_data:UserCreation,sesh:sessionDep):
    exists=await get_user_by_username(sesh,user_data.username)
    if exists:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system.",
        )
    user=await create_user(sesh,user_data)
    return user

@router.post("/login")
async def login(form_data:Annotated[OAuth2PasswordRequestForm,Depends()],sesh:sessionDep):
    password=form_data.password
    username=form_data.username
    user=await get_user_by_username(sesh,username)
    if not user: 
        raise error_types.INVALID_CRED_ERROR
    if not verify_password(password,user.hashed_password):
        raise error_types.INVALID_CRED_ERROR
    
    access_token=create_access_token(user.username)

    return {"access_token":access_token,"token_type": "bearer"}
    

@router.post("/login")
async def login(form_data:Annotated[OAuth2PasswordRequestForm,Depends()],sesh:sessionDep):
    password=form_data.password
    username=form_data.username
    user=await get_user_by_username(sesh,username)
    if not user: 
        raise error_types.INVALID_CRED_ERROR
    if not verify_password(password,user.hashed_password):
        raise error_types.INVALID_CRED_ERROR
    
    access_token=create_access_token(user.username)

    return {"access_token":access_token,"token_type": "bearer"}
    




