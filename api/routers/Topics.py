from fastapi import APIRouter, Depends, Response, status, HTTPException
from sqlalchemy.orm import Session
from ..models import Topic
from ..dependencies import get_db
from ..schemas import *
from ..crud import *

router = APIRouter(prefix="/topic")

@router.get("")
def get_testing_api(db: Session=Depends(get_db)):
    print("********")
    # res = db.execute("SELECT * FROM topics")
    # for r in res:
    #     print(r)
    res = db.query(Topic).filter(Topic.name == 'Will there be a war between US and China?').first()
    print(res.id)
    print("ENDING.............")

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
    return update_one_topic(topic.id, topic.name, topic.description, topic.creator_id, topic.num_of_debates, db)

# Delete a topic
@router.delete("/{id}")
def delete_topic(id: int, db: Session=Depends(get_db)):
    if id is None or not is_topic_existed(id, db):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Topic Not Found")
    return delete_one_topic(id, db)