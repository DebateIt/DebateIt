from sqlalchemy import update, delete
from sqlalchemy.orm import Session
from fastapi import status, Response

from .models import *
from . import schemas, auth


def seed(db: Session) -> None:
    # Empty the database
    tables = [Recording, Debate, Topic, User]
    for t in tables:
        db.execute(delete(t))
    db.commit()

    # Create Users
    alice = User(username="Alice", password=auth.pwd_context.hash("alice"))
    db.add(alice)
    bob = User(username="Bob", password=auth.pwd_context.hash("bob"))
    db.add(bob)
    eve = User(username="Eva", password=auth.pwd_context.hash("eva"))
    db.add(eve)
    Admin = User(username="Admin", password=auth.pwd_context.hash("admin"))
    db.add(Admin)

    db.commit()
    db.refresh(alice)
    db.refresh(bob)
    db.refresh(eve)

    # Create Topics
    slur = Topic(
        name="Should we ban racial slur on social media?",
        description="asdfasdfasdfasfd",
        creator_id=alice.id,
    )
    db.add(slur)
    us_china = Topic(
        name="Will there be a war between US and China?",
        description="asdfasdfasdfasdfasfd",
        creator_id=bob.id,
    )
    db.add(us_china)
    feminism = Topic(
        name="Is feminism about female dominance?",
        description="asdfasdfasdfasdfas",
        creator_id=eve.id,
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


def create_one_topic(
    name: str, description: str, creator_id: int, num_of_debates: int, db: Session
) -> Topic:
    new_topic = Topic(
        name=name,
        description=description,
        creator_id=creator_id,
        num_of_debates=num_of_debates,
    )

    db.add(new_topic)
    db.commit()
    db.refresh(new_topic)

    return new_topic


def get_one_topic(id: int, db: Session) -> Topic:
    return db.query(Topic).filter(Topic.id == id).first()


def update_one_topic(id: int, topic: schemas.UpdateTopic, db: Session) -> Topic:
    # if the topic is still use the old name, skip checking
    # else, check whether the new name is in use
    if topic.name != None:
        if topic.name != db.query(Topic).filter(Topic.id == id).first().name:
            if is_topic_name_existed(topic.name, db):
                return False

    stmt = (
        update(Topic)
        .where(Topic.id == id)
        .values(**(topic.dict(exclude_unset=True)))
        .execution_options(synchronize_session="fetch")
    )
    db.execute(stmt)
    db.commit()

    return db.query(Topic).filter(Topic.id == id).first()


def delete_one_topic(id: int, db: Session):
    if id is None or not is_topic_existed(id, db):
        return False

    db.query(Topic).filter(Topic.id == id).delete(synchronize_session="fetch")
    db.commit()
    return True


def IsUserExist(username, db: Session) -> bool:
    if username is None:
        return False
    existance = db.query(User).filter(User.username == username)
    return db.query(existance.exists()).scalar()

#For the return type of this one
def getAllUsers(db: Session) -> list[User]:
    return db.query(User).all()


def getOneUser(username: str, db: Session) -> User:
    return db.query(User).filter(User.username == username).first()


def delOneUser(username: str, db: Session) -> Response:
    db.query(User).filter(User.username == username).delete(synchronize_session="fetch")
    db.commit()
    return Response(
        status_code=status.HTTP_200_OK, content=f"User {username} is deleted"
    )


def updateOneUser(
    db: Session, username: str, new_user: schemas.UpdateUserPydantic
) -> User:
    if new_user.new_password is not None:
        db.query(User).filter(User.username == username).update(
            {"password": new_user.new_password}, synchronize_session="fetch"
        )

    if new_user.new_username is not None:
        db.query(User).filter(User.username == username).update(
            {"username": new_user.new_username}, synchronize_session="fetch"
        )
        username = new_user.new_username

    db.commit()

    return db.query(User).filter(User.username == username).first()


def addOneUser(username: str, password: str, db: Session) -> User:
    new_user = User(username=username, password=auth.pwd_context.hash(password))

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
    
def IsDebateIdExist(id,db) -> bool:
    res = db.query(Debate).filter(Debate.id == id)
    return db.query(res.exists()).scalar()

def getOneDebate(id,db) -> Debate:
    return db.query(Debate).filter(Debate.id == id).first()

def addOneDebate(userId:int,payload:schemas.Debate,db:Session) -> Debate:
    topic_info = get_one_topic(payload.topic_id,db)
    new_num = topic_info.num_of_debates +1

    update_one_topic(payload.topic_id,schemas.UpdateTopic(num_of_debates=new_num),db)

    if payload.as_pro:
        new_Debate = Debate(topic_id=payload.topic_id,
            nth_time_of_debate=new_num,
            pro_user_id =userId,)
    elif payload.as_con:
        new_Debate = Debate(topic_id=payload.topic_id,
            nth_time_of_debate=new_num,
            con_user_id=userId)

    db.add(new_Debate)
    db.commit()
    db.refresh(new_Debate)

    return new_Debate

def delOneDebate(id,db:Session)->None:
    db.query(Debate).filter(Debate.id == id).delete(synchronize_session="fetch")
    db.commit()
    

def updateOneDebate(payload:schemas.UpdateDebate,db:Session) -> Debate:
    db.query(Debate).filter(Debate.id == payload.id).update(
            {"start_time": payload.new_start_time,
            "first_recording_id":payload.new_first_recording_id,
            "last_recording_id":payload.new_last_recording_id}
            , synchronize_session="fetch"
        )
    db.commit()
    return getOneDebate(payload.id,db)
    
def userJoinDebate(userID,payload,db) -> Debate:
    if payload.as_pro:
        db.query(Debate).filter(Debate.id == payload.id).update(
            {"pro_user_id": userID}, synchronize_session="fetch"
        )
    elif payload.as_con:
        db.query(Debate).filter(Debate.id == payload.id).update(
            {"con_user_id": userID}, synchronize_session="fetch"
        )

    db.commit()

    return getOneDebate(payload.id,db)

# 后面要继续改，处理结束debate和离开debate的问题
def userExitDebate(userID,payload,db):
    if payload.as_pro:
        db.query(Debate).filter(Debate.id == payload.id).update(
            {"pro_user_id": None}, synchronize_session="fetch"
        )
    elif payload.as_con:
        db.query(Debate).filter(Debate.id == payload.id).update(
            {"con_user_id": None}, synchronize_session="fetch"
        )

    db.commit()

    new_deb = getOneDebate(payload.id,db)
    if new_deb.con_user_id is None and new_deb.pro_user_id is None:
        return delOneDebate(new_deb.id,db)
    else:
        return new_deb