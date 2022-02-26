from typing import Optional
from pydantic import BaseModel, validator, Field
from .database import SessionLocal
from typing import Optional
from fastapi import HTTPException, status
from . import crud, auth


class Topic(BaseModel):
    id: Optional[int] = None
    name: str
    description: Optional[str] = None
    creator_id: int
    num_of_debates: Optional[int] = Field(0, ge=0)


class CreateTopic(Topic):
    # topic id will not be checked
    # since id will be automatically assigned to a new topic

    @validator("creator_id")
    def is_creator_valid(cls, v):
        if v is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Please Provide the Topic Creator",
            )
        db = SessionLocal()
        if not crud.is_user_existed_by_id(v, db):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No Record of the Topic Creator",
            )
        db.close()
        return v

    @validator("name")
    def check_topic_name_existed(cls, v):
        if v is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Please Provide the Topic Name",
            )
        db = SessionLocal()
        if crud.is_topic_name_existed(v, db):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Topic Name Already Exist",
            )
        db.close()
        return v


class UpdateTopic(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    creator_id: Optional[int] = None
    num_of_debates: Optional[int] = Field(ge=0)

    @validator("creator_id")
    def is_creator_valid(cls, v):
        if v is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Please Provide the Topic Creator",
            )
        db = SessionLocal()
        if not crud.is_user_existed_by_id(v, db):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No Record of the Topic Creator",
            )
        db.close()
        return v


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


class UserLogin(UserPydantic):
    @validator("username")
    def CheckNameExist(cls, v):
        db = SessionLocal()
        if not crud.IsUserExist(v, db):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Username or Password"
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
        return auth.pwd_context.hash(v)


class Token(BaseModel):
    token_content: str
    token_type: str


class TokenData(BaseModel):
    id: int
    username: str
