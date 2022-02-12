from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from ..dependencies import get_db
from ..models import User
from .. import schemas
from ..crud import *

router = APIRouter()


@router.post("/user", status_code=status.HTTP_201_CREATED)
def add_new_user(
    payload: schemas.CreateUserPydantic,
    db: Session = Depends(get_db),
) -> schemas.UserPydantic:
    return addOneUser(payload.username, payload.password, db)


@router.get("/user/all")
def get_all_user_info(db: Session = Depends(get_db)):
    return getAllUsers(db)


@router.get("/user/{username}")
def get_user_info(username: str, db: Session = Depends(get_db)) -> User:
    if not IsUserExist(username, db):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"User Not Found"
        )
    return getOneUser(username, db)


@router.delete("/user/{username}")
def del_user(username: str, db: Session = Depends(get_db)):
    if not IsUserExist(username, db):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"User Not Found"
        )
    return delOneUser(username, db)


@router.put("/user/{username}")
def change_passwd(
    username: str, payload: schemas.UpdateUserPydantic, db: Session = Depends(get_db)
) -> User:
    if not IsUserExist(username, db):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"User Not Found"
        )
    return updateOneUser(
        db=db,
        username=username,
        new_username=payload.new_username,
        new_password=payload.new_password,
    )
