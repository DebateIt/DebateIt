from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from ..dependencies import get_db
from .. import models
from .. import schemas, auth
from ..crud import updateOneDebate, addOneDebate, userJoinDebate, \
    getOneDebate, userExitDebate, IsDebateIdExist, delOneDebate

router = APIRouter(prefix="/debate")


@router.post("", status_code=status.HTTP_201_CREATED)
def add_new_debate(
    payload: schemas.Debate,
    db: Session = Depends(get_db),
    currUser: schemas.TokenData = Depends(auth.getCurrentUser),
) -> models.Debate:
    return addOneDebate(currUser.id, payload, db)


@router.post("/join", status_code=status.HTTP_200_OK)
def join_debate(
    payload: schemas.JoinDebate,
    db: Session = Depends(get_db),
    currUser: schemas.TokenData = Depends(auth.getCurrentUser),
) -> models.Debate:
    return userJoinDebate(currUser.id, payload, db)


@router.post("/exit", status_code=status.HTTP_200_OK)
def leave_debate(
    payload: schemas.ExitDebate,
    db: Session = Depends(get_db),
    currUser: schemas.TokenData = Depends(auth.getCurrentUser),
):
    # Make sure the one want to leave is in the debate
    theDebate = getOneDebate(payload.id, db)
    if payload.as_pro:
        if currUser.id != theDebate.pro_user_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Pro User Doesn't Match",
            )
    elif payload.as_con:
        if currUser.id != theDebate.con_user_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Con User Doesn't Match",
            )

    return userExitDebate(currUser.id, payload, db)


@router.get("/{id}")
def get_debate_info(id: int, db: Session = Depends(get_db)) -> models.Debate:
    if not IsDebateIdExist(id, db):

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Debate Not Found"
        )

    return getOneDebate(id, db)


@router.delete("/{id}")
def del_debate(
    id: int,
    db: Session = Depends(get_db),
    currUser: schemas.TokenData = Depends(auth.getCurrentUser),
) -> Response:
    if currUser.username != "Admin":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Only Admin can delete debate",
        )

    res = delOneDebate(id, db)
    if res:
        return Response(
            status_code=status.HTTP_200_OK, content=f"Debate {id} is deleted"
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="delete failed",
        )


@router.put("")
def update_debate(
    payload: schemas.UpdateDebate,
    db: Session = Depends(get_db),
) -> models.Debate:
    return updateOneDebate(db=db, payload=payload)
