from fastapi import  Depends, HTTPException, status,APIRouter
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from ..dependencies import get_db
from ..models import Message
from .. import schemas, auth, crud

router = APIRouter(prefix="/room")

def determine_turn(debate_id:int, db: Session) -> bool:
    switch = crud.getOneSwitch(debate_id,db)
    number = db.query(Message).filter(Message.debate_id == debate_id).count()
    return bool((number+1 + int(switch)) % 2)


@router.get("/history/{debateID}")
def get_debate_history(debateID:int,db: Session = Depends(get_db)):
    return (
        db.query(Message)
        .filter(Message.debate_id == debateID)
        .order_by(Message.id)
        .all()
    )

@router.get("/initialize/{debateID}")
def initialize_room(debateID:int,db: Session = Depends(get_db)):
    return {"pro_turn":determine_turn(debateID,db),"debate_id":debateID}

# TODO 
# 需要写一个Next多少多少条的
#  
# TODO 
# 以后需要在数据表里加入message对另外的message的引用

@router.get("/switch/{debate_id}")
def switch_turn_algo(debate_id:int,
    db: Session = Depends(get_db),
    currUser: schemas.TokenData = Depends(auth.getCurrentUser)) -> dict:
    curr_turn = determine_turn(debate_id,db)
    curr_deb = crud.getOneDebate(debate_id,db)
    if (curr_turn and curr_deb.pro_user_id != currUser.id) or \
        (not curr_turn and curr_deb.con_user_id != currUser.id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User #{currUser.id} cannot send message in this turn!",
        )

    crud.updateSwitch(debate_id,db,not curr_deb.switched)

    return {"pro_turn":determine_turn(debate_id,db),"debate_id":debate_id}


@router.post("/message")
def send_message(
    payload: schemas.Message,
    db: Session = Depends(get_db),
    currUser: schemas.TokenData = Depends(auth.getCurrentUser),
) -> dict:
    curr_turn = determine_turn(payload.debate_id,db)
    if payload.pro_turn is not curr_turn:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Turn Match Error",
        )
    curr_deb = crud.getOneDebate(payload.debate_id,db)
    if (payload.pro_turn and curr_deb.pro_user_id != currUser.id) or \
        (not payload.pro_turn and curr_deb.con_user_id != currUser.id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User #{currUser.id} cannot send message in this turn!",
        )


    new_message = Message(
        content=payload.content, debate_id=payload.debate_id, user_id=currUser.id
    )
    db.add(new_message)
    db.commit()
    db.refresh(new_message)

    return {"pro_turn":determine_turn(payload.debate_id,db),"debate_id":payload.debate_id}
