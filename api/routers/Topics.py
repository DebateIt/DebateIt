from fastapi import APIRouter, Depends, Response,status,HTTPException
from sqlalchemy.orm import Session
from .. import models
from ..database import get_db

from ..schemas import Topic

router = APIRouter()

# validate inputs from frontend
def topic_validator(name: str, description: str, creator_id: id, num_of_debates: id):
    if creator_id < 1:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Invalid input of creator id")
    if num_of_debates < 0:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Invalid input of number of debates")

# Create a topic
@router.post("/topic/", status_code=status.HTTP_201_CREATED)
def create_topic(topic: Topic, db: Session=Depends(get_db)):
    topic_validator(topic.name, topic.description, topic.creator_id, topic.num_of_debates)

    res = db.query(models.Topic).filter(models.Topic.name == topic.name).first()
    if res is not None:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Topic already existed")

    # Ignore user input of id if provided
    topic.id = None
    newTopic = models.Topic(**topic.dict())
    db.add(newTopic)
    db.commit()
    db.refresh(newTopic)

    return {
        "success": "true",
        "msg": "Create a topic",
        "topic": topic
    }

# Get one topic profile
@router.get("/topic/{id}")
def get_topic(id: int, db: Session=Depends(get_db)):
    res = db.query(models.Topic).filter(models.Topic.id == id).first()
    if res is None:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Topic not Found")
    else:
        return {
            "success": "true",
            "msg": f"Get the #{id} topic",
            "topic": res
        }

# Update one topic profile
@router.put("/topic/")
def update_topic(topic: Topic, db: Session=Depends(get_db)):
    topic_validator(topic.name, topic.description, topic.creator_id, topic.num_of_debates)

    res = db.query(models.Topic).filter(models.Topic.id == topic.id).first()
    if res is None:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Topic not Found; Failed to be Updated")

    res = db.query(models.Topic).filter(models.Topic.name == topic.name).first()
    if res is not None:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Topic Name already Existed")

    db.query(models.Topic).filter(models.Topic.id == topic.id)\
        .update({"name":topic.name, "description":topic.description, "creator_id":topic.creator_id,
                 "num_of_debates":topic.num_of_debates}, synchronize_session='fetch')
    db.commit()

    return {
        "success": "true",
        "msg": f"Update the #{topic.id} topic"
    }

# Delete a topic
@router.delete("/topic/")
def delete_topic(topic: Topic, db: Session=Depends(get_db), status_code=status.HTTP_200_OK):
    if topic.id < 1:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Invalid input of topic id")

    res = db.query(models.Topic).filter(models.Topic.id == topic.id).first()
    if res is None:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Topic not Found; Failed to be Deleted")

    db.query(models.Topic).filter(models.Topic.id == topic.id).delete(synchronize_session='fetch')
    db.commit()

    return {
            "success": "true",
            "msg": f"Delete the #{topic.id} topic "
        }