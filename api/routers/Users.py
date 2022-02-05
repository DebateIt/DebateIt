import imp
from fastapi import APIRouter, Depends, Response,status,HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models
from .router_models import UserPydantic
from passlib.context import CryptContext
import time

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/add_user",status_code=status.HTTP_201_CREATED)
def add_new_user(payload:UserPydantic, db: Session= Depends(get_db)):
    if payload.password is None or payload.password == "":
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,detail="Invalid Password")
    
    existance = db.query(models.User).filter(models.User.username == payload.username).first()
    if existance is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Username Already Exist")
    #还需要加别的检验吗？
    new_user = models.User(**payload.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return{"data":new_user}

@router.get("/all_user")
def get_all_user_info(db: Session= Depends(get_db)):
    all_users = db.query(models.User).all()
    return {"data":all_users}

@router.get("/user/{username}")
def get_user_info(username:str, db: Session= Depends(get_db)):
    if username is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid username")
    
    existance = db.query(models.User).filter(models.User.username == username).first()
    if existance is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User Not Exist")
    else:
        return {"data":existance}

@router.delete("/user/{username}")
def del_user(username:str, db: Session= Depends(get_db)):
    if username is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid username")
    existance = db.query(models.User)\
            .filter(models.User.username == username).first()
    if existance is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User Not Exist")
    db.query(models.User).filter(models.User.username == username)\
            .delete(synchronize_session='fetch')
    db.commit()
    return Response(status_code=status.HTTP_200_OK,content=f"User {username} is deleted")

@router.put("/user/change")
def change_passwd(payload:UserPydantic, db: Session= Depends(get_db)):
    if payload.password is None or payload.password == "":
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,detail="Invalid Password")

    if payload is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid Info")

    existance = db.query(models.User).filter(models.User.username == payload.username).first()
    if existance is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User Not Exist")
    db.query(models.User).filter(models.User.username == payload.username)\
            .update({"password":payload.password},synchronize_session='fetch')
    db.commit()

    db.refresh(existance)
    return {"data":existance}

