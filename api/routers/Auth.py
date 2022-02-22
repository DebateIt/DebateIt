from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from ..dependencies import get_db
from .. import schemas, auth
from .. import crud

router = APIRouter()


@router.post("/login")
def login(userCred: schemas.UserLogin, db: Session = Depends(get_db)):
    userDB = crud.getOneUser(userCred.username, db)
    if not auth.verify_password(userCred.password, userDB.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Invalid Username or Password",
        )
    access_token = auth.create_access_token(
        data={"username": userDB.username, "id": userDB.id}
    )
    return schemas.Token(token_content=access_token, token_type="bearer")
