from fastapi import APIRouter, Depends, Response, status, HTTPException
from sqlalchemy.orm import Session
from ..models import Topic
from ..dependencies import get_db
from ..schemas import *
from ..crud import *

router = APIRouter(prefix="/topic")

# check whether the user of "creator_id" owns the topic of "topic_id"
def own_topic(topic_id: int, creator_id: int, db: Session):
    if creator_id != db.query(Topic).filter(Topic.id == topic_id).first().creator_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Topic Not Created by the Current User",
        )


# Create one topic
@router.post("", status_code=status.HTTP_201_CREATED)
def create_topic(
    topic: CreateTopic,
    db: Session = Depends(get_db),
    currUser: schemas.TokenData = Depends(auth.getCurrentUser),
) -> Topic:
    return create_one_topic(
        topic.name, topic.description, currUser.id, topic.num_of_debates, db
    )


# Get one topic profile
@router.get("/{topic_id}")
def get_topic(topic_id: int, db: Session = Depends(get_db)) -> Topic:
    if topic_id is None or not is_topic_existed(topic_id, db):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Topic Not Found"
        )
    return get_one_topic(topic_id, db)


# Update one topic profile
@router.put("/{topic_id}")  # topic_id
def update_topic(
    topic_id: int,
    topic: UpdateTopic,
    db: Session = Depends(get_db),
    currUser: schemas.TokenData = Depends(auth.getCurrentUser),
) -> Topic:
    if topic_id is None or not crud.is_topic_existed(topic_id, db):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Topic Not Found"
        )

    # if the topic still uses the old name, skip checking
    # else, check whether the new name is in use
    if topic.name != None:
        if topic.name != db.query(Topic).filter(Topic.id == topic_id).first().name:
            if is_topic_name_existed(topic.name, db):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Topic Name Already Exist",
                )

    # check whether the user of "currUser.id" owns the topic of "topic_id"
    own_topic(topic_id, currUser.id, db)

    res = update_one_topic(topic_id, topic, db)
    return res


# Delete a topic
@router.delete("/{topic_id}")
def delete_topic(
    topic_id: int,
    db: Session = Depends(get_db),
    currUser: schemas.TokenData = Depends(auth.getCurrentUser),
) -> Response:
    if topic_id is None or not crud.is_topic_existed(topic_id, db):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Topic Not Found"
        )

    # check whether the user of "currUser.id" owns the topic of "topic_id"
    own_topic(topic_id, currUser.id, db)

    if delete_one_topic(topic_id, db):
        return Response(
            status_code=status.HTTP_200_OK, content=f"Topic #{topic_id} is deleted."
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Topic Not Found"
        )


@router.get("/ownedby/{user_id}")
def get_mine_topics(user_id: int, db: Session = Depends(get_db)) -> list[Topic]:
    return read_mine_topics(user_id=user_id, db=db)
