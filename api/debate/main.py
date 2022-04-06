from typing import Optional
from pydantic import BaseModel
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from ..dependencies import get_db
from ..models import Message
from . import schemas

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

PRO_USER_ID = 1
CON_USER_ID = 2
DEBATE_ID = 1

curr_turn = PRO_USER_ID


@app.get("/history")
def get_debate_history(db: Session = Depends(get_db)):
    return (
        db.query(Message)
        .filter(Message.debate_id == DEBATE_ID)
        .order_by(Message.id)
        .all()
    )


@app.post("/message")
def send_message(
    payload: schemas.Message,
    db: Session = Depends(get_db),
):
    global curr_turn

    if curr_turn != payload.user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User #{payload.user_id} cannot send message in this turn!",
        )
    new_message = Message(
        content=payload.content, debate_id=DEBATE_ID, user_id=payload.user_id
    )
    db.add(new_message)
    db.commit()
    db.refresh(new_message)

    curr_turn = PRO_USER_ID if curr_turn != PRO_USER_ID else CON_USER_ID
    return new_message
