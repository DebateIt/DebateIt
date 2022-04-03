from typing import Optional
from pydantic import BaseModel
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from ..dependencies import get_db
from ..import models

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

PRO_USER_ID = None
CON_USER_ID = None
DEBATE_ID = 1

curr_turn = None


class Message(BaseModel):
    id: Optional[int] = None
    content: str
    debate_id: Optional[int] = None
    user_id: int


@app.get("/history")
def get_debate_history(db: Session = Depends(get_db)):
    return db.query(models.Message).filter(
        models.Message.debate_id == DEBATE_ID
    ).all()


@app.post("/message")
def send_message(
    payload: Message,
    db: Session = Depends(get_db),
):
    new_message = models.Message(
        content=payload.content,
        debate_id=DEBATE_ID,
        user_id=payload.user_id
    )
    db.add(new_message)
    db.commit()
    db.refresh()

    return new_message
