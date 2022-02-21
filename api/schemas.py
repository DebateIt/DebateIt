from typing import Optional
from pydantic import BaseModel, validator, Field
from .database import SessionLocal
from typing import Optional
from fastapi import HTTPException, status
from . import crud

class Topic(BaseModel):
    id: Optional[int] = None
    name: str
    description: Optional[str] = None
    creator_id: int
    num_of_debates: int = Field(ge=0)
#
class CreateTopic(Topic):
    # topic id will not be checked
    # since id will be automatically assigned to a new topic

    @validator("creator_id")
    def is_creator_valid(cls, v):
        if v is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Please Provide the Topic Creator")
        db = SessionLocal()
        if not crud.is_user_existed_by_id(v, db):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No Record of the Topic Creator")
        db.close()
        return v

    # @validator("num_of_debates")
    # def is_num_of_debates_leq_than_0(cls, v):
    #     if v < 0:
    #         raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Invalid Input of Number of Debates")
    #     return v

    @validator("name")
    def check_topic_name_existed(cls, v):
        if v is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Please Provide the Topic Name")
        db = SessionLocal()
        if crud.is_topic_name_existed(v, db):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Topic Name Already Exist")
        db.close()
        return v

class UpdateTopic(Topic):
    @validator("creator_id")
    def is_creator_valid(cls, v):
        if v is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Please Provide the Topic Creator")
        db = SessionLocal()
        if not crud.is_user_existed_by_id(v, db):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No Record of the Topic Creator")
        db.close()
        return v

    # @validator("num_of_debates")
    # def is_num_of_debates_leq_than_0(cls, v):
    #     if v < 0:
    #         raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Invalid input of number of debates")
    #     return v

    @validator("id")
    def is_topic_existed_by_id(cls, v):
        db = SessionLocal()
        if id is None or not crud.is_topic_existed(v, db):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Topic Not Found")
        db.close()
        return v

    # @validator("name")
    # def check_topic_name_existed(cls, v):
    #     if v is None:
    #         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Please Provide a Topic Name")
    #     return v