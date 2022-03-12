from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from ..dependencies import get_db
from .. import models
from .. import schemas, auth
from ..crud import *

router = APIRouter(prefix="/recording")

@router.post("", status_code=status.HTTP_201_CREATED)
def add_new_rec(payload:schemas.Recording,
        db:Session= Depends(get_db),
        visitUser: schemas.TokenData = Depends(auth.getCurrentUser)
        ) -> models.Recording:
    if visitUser.username != "Admin":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Only Admin can add debate",
        )
    return addOneRec(visitUser.id, payload, db)


@router.get("/{id}")
def get_Rec_info(id: int, db: Session = Depends(get_db)) -> models.Recording:
    if not IsRecIdExist(id, db):

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Recording Not Found"
        )

    return getOneRec(id, db)

@router.delete("/{id}")
def del_Rec(
    id: int,
    db: Session = Depends(get_db),
    currUser: schemas.TokenData = Depends(auth.getCurrentUser),
) -> Response:
    if currUser.username != "Admin":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Only Admin can delete debate",
        )
    res = delOneRec(id, db)
    if res:
        return Response(
            status_code=status.HTTP_200_OK, content=f"Recording {id} is deleted"
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"delete failed",
        )

# This One serves as regular link Rec to prev&next
# Usually being used, a seperate update will serve as
# Rec editor & Admin usage
@router.post("/link", status_code=status.HTTP_200_OK)
def link_Rec(payload:schemas.LinkRecording,
        db:Session= Depends(get_db),
        visitUser: schemas.TokenData = Depends(auth.getCurrentUser)) -> models.Recording:
        if visitUser.username != "Admin":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Only Admin can link debate",
            )
        return linkRecs(visitUser.id, payload, db)