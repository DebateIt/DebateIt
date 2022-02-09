from fastapi import APIRouter, Depends,status,HTTPException
from sqlalchemy.orm import Session
from ..dependencies import get_db
from ..models import User
from .. import schemas
from ..crud import *

router = APIRouter()
 
@router.post("/user",status_code=status.HTTP_201_CREATED)
def add_new_user(
    payload:schemas.CreateUserPydantic, 
    db: Session= Depends(get_db),
    ) -> schemas.UserPydantic: 
    return addOneUser(payload.username,payload.password,db)

@router.get("/user/all")
def get_all_user_info(db: Session= Depends(get_db)):
    return getAllUsers(db)

@router.get("/user/{username}")
def get_user_info(username:str, db: Session= Depends(get_db)) -> User:
    if not IsUserExist(username,db):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid Username or Password")
    return getOneUser(username,db)

@router.delete("/user/{username}")
def del_user(username:str, db: Session= Depends(get_db)):
    if not IsUserExist(username,db):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid Username or Password")
    return delOneUser(username,db)

@router.put("/user")
def change_passwd(
    payload:schemas.UpdateUserPydantic, 
    db: Session= Depends(get_db)
    ) -> User:
    return updateOneUser(payload.username,payload.password,db)

