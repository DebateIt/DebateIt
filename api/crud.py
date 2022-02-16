from sqlalchemy import delete
from sqlalchemy.orm import Session
from fastapi import status, Response
from .models import *

def seed(db: Session) -> None:
    # Empty the database
    tables = [Recording, Debate, Topic, User]
    for t in tables:
        db.execute(delete(t))
    db.commit()

    # Create Users
    alice = User(username="Alice", password="12345")
    db.add(alice)
    bob = User(username="Bob", password="1234125")
    db.add(bob)
    eve = User(username="Eve", password="13412423")
    db.add(eve)

    db.commit()
    db.refresh(alice)
    db.refresh(bob)
    db.refresh(eve)

    # Create Topics
    slur = Topic(
        name = "Should we ban racial slur on social media?",
        description = "asdfasdfasdfasfd",
        creator_id = alice.id,
    )
    db.add(slur)
    us_china = Topic(
        name = "Will there be a war between US and China?",
        description = "asdfasdfasdfasdfasfd",
        creator_id = bob.id,
    )
    db.add(us_china)
    feminism = Topic(
        name = "Is feminism about female dominance?",
        description = "asdfasdfasdfasdfas",
        creator_id = eve.id,
    )
    db.add(feminism)

    db.commit()
    db.refresh(slur)
    db.refresh(us_china)
    db.refresh(feminism)

def is_user_existed_by_id(id, db: Session) -> bool:
    res = db.query(User).filter(User.id == id)
    return db.query(res.exists()).scalar()

def is_topic_existed(id, db: Session) -> bool:
    res = db.query(Topic).filter(Topic.id == id)
    return db.query(res.exists()).scalar()

def is_topic_name_existed(name, db: Session) -> bool:
    res = db.query(Topic).filter(Topic.name == name)
    return db.query(res.exists()).scalar()

def create_one_topic(name: str, description: str, creator_id: int, num_of_debates: int, db: Session) -> Topic:
    new_topic = Topic(id=None, name=name, description=description,
                      creator_id=creator_id, num_of_debates=num_of_debates)

    db.add(new_topic)
    db.commit()
    db.refresh(new_topic)

    # retrieve id using db and put it into new _topic
    res = db.query(Topic).filter(Topic.name == name).first()
    new_topic.id = res.id

    return new_topic

def get_one_topic(id: int, db: Session) -> Topic:
    return db.query(Topic).filter(Topic.id == id).first()

def update_one_topic(id: int, name: str, description: str, creator_id: int, num_of_debates: int, db: Session) -> Topic:
    # if the topic is still use the old name, skip checking
    # else, check whether the new name is in use
    if name != db.query(Topic).filter(Topic.id == id).first().name:
        if crud.is_topic_name_existed(v, db):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Topic Name Already Exist")
        else:
            db.query(Topic).filter(Topic.id == id).update({"name": name}, synchronize_session="fetch")
            db.commit()

    db.query(Topic).filter(Topic.id == id).update(
        {"description": description, "creator_id": creator_id, "num_of_debates": num_of_debates}, synchronize_session="fetch"
    )
    db.commit()

    return db.query(Topic).filter(Topic.id == id).first()

def delete_one_topic(id: int, db: Session):
    name = db.query(Topic).filter(Topic.id == id).first().name
    db.query(Topic).filter(Topic.id == id).delete(synchronize_session="fetch")
    db.commit()
    return Response(
        status_code=status.HTTP_200_OK, content=f"Topic #{id} \"{name}\" is deleted."
    )