from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from ..dependencies import get_db
from .. import models
from .. import schemas, auth
from ..crud import *

router = APIRouter(prefix="/debate")

@router.post("", status_code=status.HTTP_201_CREATED)
def add_new_debate(
    payload: schemas.Debate,
    db: Session = Depends(get_db),
    currUser: schemas.TokenData = Depends(auth.getCurrentUser)
) -> models.Debate:
    return addOneDebate(currUser.id, payload,db)

@router.post("/join", status_code=status.HTTP_200_OK)
def join_debate(
    payload: schemas.JoinDebate,
    db: Session = Depends(get_db),
    currUser: schemas.TokenData = Depends(auth.getCurrentUser)
)-> models.Debate:
    return userJoinDebate(currUser.id,payload,db)

@router.post("/exit", status_code=status.HTTP_200_OK)
def leave_debate(
    payload: schemas.ExitDebate,
    db: Session = Depends(get_db),
    currUser: schemas.TokenData = Depends(auth.getCurrentUser)
):
    return userExitDebate(currUser.id,payload,db)

@router.get("/{id}")
def get_debate_info(id: int, db: Session = Depends(get_db)) -> models.Debate:
    if not IsDebateIdExist(id, db):

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Debate Not Found"
        )

    return getOneDebate(id, db)

@router.delete("/{id}")
def del_debate(
    id:int,
    db: Session = Depends(get_db),
    currUser: schemas.TokenData = Depends(auth.getCurrentUser)
) -> Response:
    if currUser.username != "Admin":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Only Admin can delete debate")
    
    delOneDebate(id, db)
    
    return Response(
        status_code=status.HTTP_200_OK, content=f"Debate {id} is deleted"
    )

@router.put("")
def update_debate(
    payload: schemas.UpdateDebate,
    db: Session = Depends(get_db),
) -> Debate:
    return updateOneDebate(db=db, payload=payload)

