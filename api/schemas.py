from .database import SessionLocal
from pydantic import BaseModel, validator
from typing import Optional
from fastapi import HTTPException, status
from . import crud


class UserPydantic(BaseModel):
    id: Optional[int] = None
    username: str
    password: str

    @validator("password")
    def passwd_cannot_be_None(cls, v):
        if v is None or v == "":
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Invalid Password"
            )
        return v


class CreateUserPydantic(UserPydantic):
    @validator("username")
    def CheckNameExist(cls, v):
        db = SessionLocal()
        if crud.IsUserExist(v, db):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Username Already Exist"
            )
        db.close()
        return v


class UpdateUserPydantic(BaseModel):
    new_username: Optional[str] = None
    new_password: Optional[str] = None

    @validator("new_username")
    def CheckNameExist(cls, v):
        db = SessionLocal()
        if crud.IsUserExist(v, db):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Username Already Exist"
            )
        db.close()
        return v

    @validator("new_password")
    def passwd_cannot_be_None(cls, v):
        if v is None or v == "":
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Invalid Password"
            )
        return v
