from typing import Optional
from pydantic import BaseModel

class Topic(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    description: Optional[str] = None
    creator_id: Optional[int] = None
    num_of_debates: Optional[int] = None
