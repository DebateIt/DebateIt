from .database import Base
from pydantic import BaseModel,validator,ValidationError
from typing import Optional
from fastapi import HTTPException,status

class UserPydantic(BaseModel):
    id:Optional[int] = None
    username:str
    password:str

    @validator('password')
    def passwd_cannot_be_None(cls,v):
        if v is None or v == "":
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,detail="Invalid Password")
        return v


