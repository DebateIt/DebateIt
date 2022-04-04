from typing import Optional
from pydantic import BaseModel


class Message(BaseModel):
    id: Optional[int] = None
    content: str
    debate_id: Optional[int] = None
    user_id: int
