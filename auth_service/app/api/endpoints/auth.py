from fastapi import APIRouter,HTTPException
from app.db.database import sessionDep
from app.db.models import User
from  sqlmodel import select
from app.core.security import getHashedPassword,verifyPassword,createJwtToken,decodeJwtToken
from fastapi import Depends
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from app.services.auth_service import get_current_user,get_user
from fastapi import status
from app.schemas.token import Token
router=APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

@router.post("/signup")
def signUp(user:User,session:sessionDep):
    if session.exec(select(User).where(User.username==user.username)).first():
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )
    
    user.password=getHashedPassword(user.password)
    session.add(user)
    session.commit()
    session.refresh(user)
    return {
        "msg":"Signup successful",
        "token":createJwtToken(data={"user_id":user.id})
    }
    
        
# @router.post("/login")
# def login(user:User,session:sessionDep):
    
#     res=session.exec(select(User).where(User.username==user.username)).first()
#     if not res:
#         raise HTTPException(
#             status_code=404,
#             detail="User with this email does not exist"
#         )
#     if not verifyPassword(user.password,res.password):
#         raise HTTPException(
#             status_code=401,
#             detail="Invalid password"
#         )
#     jwt_token=createJwtToken(data={"user_id":res.id})
#     if jwt_token is None:
#         raise HTTPException(
#             status_code=500,
#             detail="Internal server error"
#         )
#     return {
#         "msg":"Login successful",
#         "token":jwt_token
#     }
    
    
@router.post("/login",response_model=Token)
def login(session:sessionDep,form_data:OAuth2PasswordRequestForm = Depends()):
    invalid_cred_exception=HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED
            ,detail="Invalid credentilas"
        )
    username = form_data.username
    password = form_data.password
    if username is None or password is None:
        raise invalid_cred_exception
    
    user=get_user(username,session)
    if not verifyPassword(password,user.password):
        raise invalid_cred_exception
    
    new_token=createJwtToken(data={"sub":username})
    if not new_token:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error"
        )
    token_obj=Token(access_token=new_token)
    return token_obj
    

@router.post("/deleteUser")
def deleteUser(user:User,session:sessionDep):
  
    res=session.exec(select(User).where(User.username==user.username)).first()
    if not res: 
        raise HTTPException(
            status_code=404,
            detail="No such user"
        ) 
    if not verifyPassword(user.password,res.password):
        raise HTTPException(
            status_code=401,
            detail="Invalid password"
        )
    session.delete(res)
    session.commit()
    return {
        "msg":"User deleted successfully"
    }



@router.get("/test_loged_in_Status")
def read_items(user:Annotated[User,Depends(get_current_user)]):
    return {"user":user}