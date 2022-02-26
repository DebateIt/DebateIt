from fastapi import APIRouter, Depends, Response, status, HTTPException
from sqlalchemy.orm import Session
from ..models import Topic
from ..dependencies import get_db
from ..schemas import *
from ..crud import *

router = APIRouter(prefix="/topic")

def is_user_creator_matched(userId: int, creatorId: int):
    if userId != creatorId:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User and Creator Unmatched"
        )

# Create one topic
@router.post("", status_code=status.HTTP_201_CREATED)
def create_topic(topic: CreateTopic, db: Session = Depends(get_db),
                 currUser: schemas.TokenData = Depends(auth.getCurrentUser)) -> Topic:
    is_user_creator_matched(topic.creator_id, currUser.id)
    return create_one_topic(
        topic.name, topic.description, topic.creator_id, topic.num_of_debates, db
    )


# Get one topic profile
@router.get("/{id}")
def get_topic(id: int, db: Session = Depends(get_db)) -> Topic:
    if id is None or not is_topic_existed(id, db):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Topic Not Found"
        )
    return get_one_topic(id, db)


# Update one topic profile
@router.put("/{id}")
def update_topic(id: int, topic: UpdateTopic, db: Session = Depends(get_db),
                 currUser: schemas.TokenData = Depends(auth.getCurrentUser)):
    is_user_creator_matched(topic.creator_id, currUser.id)
    if id is None or not crud.is_topic_existed(id, db):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Topic Not Found"
        )

    res = update_one_topic(id, topic, db)
    if not res:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Topic Name Already Exist"
        )
    else:
        return res


# Delete a topic
@router.delete("/{id}")
def delete_topic(id: int, topic: DeleteTopic, db: Session = Depends(get_db),
                 currUser: schemas.TokenData = Depends(auth.getCurrentUser)):
    is_user_creator_matched(topic.creator_id, currUser.id)
    if delete_one_topic(id, db):
        return Response(
            status_code=status.HTTP_200_OK, content=f"Topic #{id} is deleted."
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Topic Not Found"
        )
