from ..database import Base
from pydantic import BaseModel
from typing import Optional

class UserPydantic(BaseModel):
    id:Optional[int] = None
    username:str
    password:str