
from fastapi import APIRouter, Depends,status
from sqlalchemy.orm import Session
from ..dependencies import get_db
from ..models import User
from ..schemas import UserPydantic
from passlib.context import CryptContext
from ..crud import *

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
 
@router.post("/user",status_code=status.HTTP_201_CREATED)
def add_new_user(payload:UserPydantic, db: Session= Depends(get_db)) -> UserPydantic: 
    return addOneUser(payload.username,payload.password,db)

@router.get("/user/all")
def get_all_user_info(db: Session= Depends(get_db)):
    return getAllUsers(db)

@router.get("/user/{username}")
def get_user_info(username:str, db: Session= Depends(get_db)) -> User:
    return getOneUser(username,db)

@router.delete("/user/{username}")
def del_user(username:str, db: Session= Depends(get_db)):
    return delOneUser(username,db)

@router.put("/user")
def change_passwd(payload:UserPydantic, db: Session= Depends(get_db)) -> User:
    return updateOneUser(payload.username,payload.password,db)

