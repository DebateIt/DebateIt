from typing import Optional
from pydantic import BaseModel, validator, root_validator, Field
from .database import SessionLocal
from typing import Optional
from fastapi import HTTPException, status
from . import crud, auth
from datetime import datetime


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
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid Username or Password",
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


class Debate(BaseModel):
    id: Optional[int] = None
    topic_id: int
    as_pro: Optional[bool] = None
    as_con: Optional[bool] = None
    start_time: Optional[datetime] = None
    nth_time_of_debate: Optional[int] = None

    @validator("topic_id")
    def check_topic_existance(cls, v):
        db = SessionLocal()
        if not crud.is_topic_existed(v, db):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Topic Not Exist"
            )
        db.close()
        return v


class UpdateDebate(BaseModel):
    id: int
    new_start_time: Optional[int] = None
    new_first_recording_id: Optional[int] = None
    new_last_recording_id: Optional[int] = None

    @validator("id")
    def check_debateID_existance(cls, v):
        db = SessionLocal()
        if not crud.IsDebateIdExist(v, db):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Debate Not Exist"
            )
        db.close()
        return v


class JoinDebate(BaseModel):
    id: int
    as_pro: Optional[bool] = None
    as_con: Optional[bool] = None

    @validator("id")
    def check_debateID_existance(cls, v):
        db = SessionLocal()
        if not crud.IsDebateIdExist(v, db):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Debate Not Exist"
            )
        db.close()
        return v

    @root_validator
    def check_user_id(cls, values):
        id = values.get("id")
        pro, con = values.get("as_pro"), values.get("as_con")
        if pro is None and con is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Pro and Con Cannot be None at same time",
            )
        elif pro and con:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Both Pro and Con Entered",
            )

        db = SessionLocal()
        debate = crud.getOneDebate(id, db)
        db.close()

        if pro is None:
            if debate.con_user_id is not None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Con Position Unavailable",
                )
            elif debate.pro_user_id == con:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="You Cannot take two sides!",
                )
            return values
        elif con is None:
            if debate.pro_user_id is not None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Pro Position Unavailable",
                )
            elif debate.con_user_id == pro:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="You Cannot take two sides!",
                )
            return values


class ExitDebate(BaseModel):
    id: int
    as_pro: Optional[bool] = None
    as_con: Optional[bool] = None

    @validator("id")
    def check_debateID_existance(cls, v):
        db = SessionLocal()
        if not crud.IsDebateIdExist(v, db):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Debate Not Exist"
            )
        db.close()
        return v

    @root_validator
    def check_different_user_id(cls, values):
        id = values.get("id")
        pro, con = values.get("as_pro"), values.get("as_con")
        if pro is None and con is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Pro and Con Cannot be None at same time",
            )
        elif pro and con:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Both Pro and Con Entered",
            )

        db = SessionLocal()
        debate = crud.getOneDebate(id, db)
        db.close()

        if pro is None:
            if debate.con_user_id is None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Con Position Is None, cannot exit",
                )
            return values
        elif con is None:
            if debate.pro_user_id is None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Pro Position is None, Cannot Exit",
                )
            return values
