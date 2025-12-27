from pydantic import BaseModel,EmailStr,ConfigDict,Field
from typing import Optional



class UserBase(BaseModel):
    email_id:EmailStr
    is_super_user:Optional[bool]=Field(default=False)
    is_active:Optional[bool]=Field(default=True)
    username:str


class UserCreation(UserBase):
    password:str

class UserResponse(UserBase):
    id:int
    
    model_config=ConfigDict(from_attributes=True)
