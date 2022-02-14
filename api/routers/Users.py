from fastapi import APIRouter, Depends,status,HTTPException
from sqlalchemy.orm import Session
from ..dependencies import get_db
from ..models import User
from .. import schemas,auth
from ..crud import *

router = APIRouter(prefix="/user")
 
@router.post("",status_code=status.HTTP_201_CREATED)
def add_new_user(
    payload:schemas.CreateUserPydantic, 
    db: Session= Depends(get_db),
    ) -> schemas.UserPydantic: 
    return addOneUser(payload.username,payload.password,db)

@router.get("/all")
def get_all_user_info(db: Session= Depends(get_db)):
    return getAllUsers(db)

@router.get("/{username}")
def get_user_info(username:str, db: Session= Depends(get_db)) -> User:
    if not IsUserExist(username,db):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User Not Found")
    return getOneUser(username,db)

@router.delete("")
def del_user(username:str, 
            db: Session= Depends(get_db),
            currUser:schemas.TokenData = Depends(auth.getCurrentUser)):
    return delOneUser(currUser.username,db)

@router.put("")
def update_user(
    username:str,
    payload:schemas.UpdateUserPydantic, 
    db: Session= Depends(get_db),
    currUser:schemas.TokenData = Depends(auth.getCurrentUser)) -> User:
    userDB = updateOneUser(db=db,username=currUser.username,new_user=payload)
    access_token = auth.create_access_token(data={"username":userDB.username,"id":userDB.id})
    return schemas.Token(token_content=access_token,token_type="bearer")