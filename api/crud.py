from sqlalchemy import delete
from sqlalchemy.orm import Session
from .models import *
from fastapi import status,Response
from . import schemas

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

def IsUserExist(username, db: Session) -> bool:
    if username is None:
        return False
    existance = db.query(User).filter(User.username == username)
    return db.query(existance.exists()).scalar()

def getAllUsers(db:Session) -> list[User]:
    return db.query(User).all()

def getOneUser(username:str,db:Session) -> User:
    return db.query(User).filter(User.username == username).first()

def delOneUser(username:str,db:Session) -> Response:
    db.query(User).filter(User.username == username)\
            .delete(synchronize_session='fetch')
    db.commit()
    return Response(status_code=status.HTTP_200_OK,content=f"User {username} is deleted")

def updateOneUser(db:Session,username:str,new_user:schemas.UpdateUserPydantic) -> User:
    if new_user.new_password is not None:
        db.query(User).filter(User.username == username)\
                .update({"password":new_user.new_password},synchronize_session='fetch')

    if new_user.new_username is not None:
        db.query(User).filter(User.username == username)\
                .update({"username":new_user.new_username},synchronize_session='fetch')
        username = new_user.new_username
    db.commit()

    return db.query(User).filter(User.username == username).first()

def addOneUser(username:str,password:str,db:Session) -> User:
    new_user = User(username=username,password=password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
