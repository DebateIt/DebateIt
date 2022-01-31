from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import crud, dependencies

router = APIRouter(prefix="/utils")

@router.get("/seed")
def seed(db: Session = Depends(dependencies.get_db)):
    crud.seed(db)
    return {
        "msg": "Success!"
    }
