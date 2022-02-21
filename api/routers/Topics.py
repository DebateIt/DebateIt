from fastapi import APIRouter, Depends, Response, status, HTTPException
from sqlalchemy.orm import Session
from ..models import Topic
from ..dependencies import get_db
from ..schemas import *
from ..crud import *

router = APIRouter(prefix="/topic")

# Create one topic
@router.post("", status_code=status.HTTP_201_CREATED)
def create_topic(topic: CreateTopic, db: Session=Depends(get_db)) -> Topic:
    return create_one_topic(topic.name, topic.description, topic.creator_id, topic.num_of_debates, db)

# Get one topic profile
@router.get("/{id}")
def get_topic(id: int, db: Session=Depends(get_db)) -> Topic:
    if id is None or not is_topic_existed(id, db):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Topic Not Found")
    return get_one_topic(id, db)

# Update one topic profile
@router.put("")
def update_topic(topic: UpdateTopic, db: Session=Depends(get_db)):
    res = update_one_topic(topic.id, topic.name, topic.description, topic.creator_id, topic.num_of_debates, db)
    if not res:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Topic Name Already Exist")
    else:
        return res

# Delete a topic
@router.delete("/{id}")
def delete_topic(id: int, db: Session=Depends(get_db)):
    if delete_one_topic(id, db):
        return Response(status_code=status.HTTP_200_OK, content=f"Topic #{id} is deleted.")
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Topic Not Found")