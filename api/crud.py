from sqlalchemy import update, delete
from sqlalchemy.orm import Session
from fastapi import status, Response, HTTPException
from datetime import datetime

from api.database import SessionLocal
from .models import *
from . import schemas, auth


def seed(db: Session) -> None:
    # Empty the database
    tables = [Message, Debate, Topic, User]
    for t in tables:
        db.execute(delete(t))
    db.commit()

    # Create Users
    alice = User(username="Alice", password=auth.pwd_context.hash("alice"))
    db.add(alice)
    bob = User(username="Bob", password=auth.pwd_context.hash("bob"))
    db.add(bob)
    eva = User(username="Eva", password=auth.pwd_context.hash("eva"))
    db.add(eva)
    Admin = User(username="Admin", password=auth.pwd_context.hash("admin"))
    db.add(Admin)

    db.commit()
    db.refresh(alice)
    db.refresh(bob)
    db.refresh(eva)

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
        creator_id=eva.id,
    )
    db.add(feminism)

    db.commit()
    db.refresh(slur)
    db.refresh(us_china)
    db.refresh(feminism)

    debate1 = Debate(
        nth_time_of_debate=1,
        start_time=datetime(2022, 5, 15, 10, 0, 0),
        status=Status.BeforeDebate,
        topic_id=slur.id,
        pro_user_id=alice.id,
        con_user_id=bob.id,
    )
    debate2 = Debate(
        nth_time_of_debate=1,
        start_time=datetime(2022, 5, 15, 10, 0, 0),
        status=Status.BeforeDebate,
        topic_id=us_china.id,
        pro_user_id=bob.id,
        con_user_id=eva.id,
    )
    db.add(debate1)
    db.add(debate2)
    db.commit()
    db.refresh(debate1)
    db.refresh(debate2)


def is_user_existed_by_id(user_id, db: Session) -> bool:
    res = db.query(User).filter(User.id == user_id)
    return db.query(res.exists()).scalar()


def is_topic_existed(topic_id, db: Session) -> bool:
    res = db.query(Topic).filter(Topic.id == topic_id)
    return db.query(res.exists()).scalar()


def is_topic_name_existed(topic_name, db: Session) -> bool:
    res = db.query(Topic).filter(Topic.name == topic_name)
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


def get_one_topic(topic_id: int, db: Session) -> Topic:
    return db.query(Topic).filter(Topic.id == topic_id).first()


def getOneTopicByName(name: str, db: Session) -> Topic:
    return db.query(Topic).filter(Topic.name == name).first()

def getAllTopics(db:Session) -> list[str]:
    return [topic[0] for topic in  db.query(Topic.name).all()]


def update_one_topic(topic_id: int, topic: schemas.UpdateTopic, db: Session) -> Topic:
    stmt = (
        update(Topic)
        .where(Topic.id == topic_id)
        .values(**(topic.dict(exclude_unset=True)))
        .execution_options(synchronize_session="fetch")
    )
    db.execute(stmt)
    db.commit()

    return db.query(Topic).filter(Topic.id == topic_id).first()


def delete_one_topic(topic_id: int, db: Session) -> bool:
    if topic_id is None or not is_topic_existed(topic_id, db):
        return False

    db.query(Topic).filter(Topic.id == topic_id).delete(synchronize_session="fetch")
    db.commit()
    return True


def IsUserExist(username, db: Session) -> bool:
    if username is None:
        return False
    existance = db.query(User).filter(User.username == username)
    return db.query(existance.exists()).scalar()


# For the return type of this one
def getAllUsers(db: Session) -> list[User]:
    return db.query(User).all()


def getOneUser(username: str, db: Session) -> User:
    return db.query(User).filter(User.username == username).first()


def delOneUser(username: str, db: Session) -> Response:
    db.query(User).filter(User.username == username).delete(synchronize_session="fetch")
    db.commit()
    return True


def updateOneUser(
    db: Session, username: str, new_user: schemas.UpdateUserPydantic
) -> User:
    update_data = new_user.dict(exclude_unset=True)
    if update_data != {}:
        db.query(User).filter(User.username == username).update(
            update_data,
            synchronize_session="fetch",
        )

        db.commit()
    new_name = new_user.username or username
    return db.query(User).filter(User.username == new_name).first()


def addOneUser(username: str, password: str, db: Session) -> User:
    new_user = User(username=username, password=auth.pwd_context.hash(password))

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def IsDebateIdExist(id, db) -> bool:
    res = db.query(Debate).filter(Debate.id == id)
    return db.query(res.exists()).scalar()


def getOneDebate(id, db) -> Debate:
    return db.query(Debate).filter(Debate.id == id).first()


def getOneDebateByTopicId(topicID: int, db: Session) -> Debate:
    # For Test Only
    return db.query(Debate).filter(Debate.topic_id == topicID).first()


def addOneDebate(userId: int, payload: schemas.Debate, db: Session) -> Debate:
    topic_info = get_one_topic(payload.topic_id, db)
    new_num = topic_info.num_of_debates + 1

    update_one_topic(payload.topic_id, schemas.UpdateTopic(num_of_debates=new_num), db)

    if payload.as_pro:
        new_Debate = Debate(
            topic_id=payload.topic_id,
            nth_time_of_debate=new_num,
            pro_user_id=userId,
        )
    elif payload.as_con:
        new_Debate = Debate(
            topic_id=payload.topic_id, nth_time_of_debate=new_num, con_user_id=userId
        )
    if payload.start_time:
        new_Debate.start_time = payload.start_time

    db.add(new_Debate)
    db.commit()
    db.refresh(new_Debate)

    return new_Debate


def delOneDebate(id, db: Session) -> bool:
    db.query(Debate).filter(Debate.id == id).delete(synchronize_session="fetch")
    db.commit()
    return True


def updateOneDebate(payload: schemas.UpdateDebate, db: Session) -> Debate:
    update_data = payload.dict(exclude_unset=True)

    if update_data != {}:
        db.query(Debate).filter(Debate.id == payload.id).update(
            update_data,
            synchronize_session="fetch",
        )
        db.commit()
    return getOneDebate(payload.id, db)


def userJoinDebate(userID, payload: schemas.JoinDebate, db: Session) -> Debate:
    # By this point, there must have been someone on one side
    # and the other side joined

    # in schemas we can't find if pro&con are the same,
    # so we need a check here
    theDebate = getOneDebate(payload.id, db)
    if payload.as_pro and theDebate.con_user_id != userID:
        db.query(Debate).filter(Debate.id == payload.id).update(
            {"pro_user_id": userID}, synchronize_session="fetch"
        )
    elif payload.as_con and theDebate.pro_user_id != userID:
        db.query(Debate).filter(Debate.id == payload.id).update(
            {"con_user_id": userID}, synchronize_session="fetch"
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot take both sides of Debate",
        )

    db.commit()

    updateOneDebate(schemas.UpdateDebate(id=payload.id, status=Status.InProgress), db)

    return getOneDebate(payload.id, db)


def userExitDebate(userID, payload: schemas.ExitDebate, db: Session):
    if payload.as_pro:
        db.query(Debate).filter(Debate.id == payload.id).update(
            {"pro_user_id": None}, synchronize_session="fetch"
        )
    elif payload.as_con:
        db.query(Debate).filter(Debate.id == payload.id).update(
            {"con_user_id": None}, synchronize_session="fetch"
        )

    db.commit()

    new_deb = getOneDebate(payload.id, db)

    # This paragraph as a whole are idealized, but after that can continue to design
    if new_deb.status is Status.End:
        # End -> Another Party Leave debate -> change status to FINISHED
        return updateOneDebate(
            schemas.UpdateDebate(id=payload.id, status=Status.Finish), db
        )
    elif (
        new_deb.status is Status.BeforeDebate
        and new_deb.con_user_id is None
        and new_deb.pro_user_id is None
    ):
        # Another Party Not Joined & Creator Leaves -> delete this debate
        return delOneDebate(new_deb.id, db)
    else:
        # Debate is over -> one party left first.
        return updateOneDebate(
            schemas.UpdateDebate(id=payload.id, status=Status.End), db
        )


# def IsRecIdExist(id, db) -> bool:
#     res = db.query(Recording).filter(Recording.id == id)
#     return db.query(res.exists()).scalar()


# def getOneRec(id: int, db: Session) -> Recording:
#     return db.query(Recording).filter(Recording.id == id).first()


# def addOneRec(userID: int, payload: schemas.Recording, db: Session) -> Recording:
#     data = payload.dict(exclude_unset=True)
#     new_Rec = Recording(**data)
#     db.add(new_Rec)
#     db.commit()
#     db.refresh(new_Rec)
#     return new_Rec


# def delOneRec(id, db: Session) -> bool:
#     theRec = getOneRec(id, db)
#     thePrevID = theRec.prev_recording_id
#     theNextID = theRec.next_recording_id

#     res = updateLink(db, prevID=thePrevID, nextID=theNextID)
#     if not res:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST, detail="Error During Updating Link"
#         )

#     db.query(Recording).filter(Recording.id == id).delete(synchronize_session="fetch")
#     db.commit()
#     return True


# def linkRecs(userID: int, payload: schemas.LinkRecording, db: Session):
#     update_data = payload.dict(exclude_unset=True)
#     if update_data != {}:
#         db.query(Recording).filter(Recording.id == payload.id).update(
#             update_data,
#             synchronize_session="fetch",
#         )
#         db.commit()
#     if payload.prev_recording_id is not None:
#         res = coLinkRecs(
#             schemas.CoLinkRecording(
#                 id=payload.prev_recording_id, next_recording_id=payload.id
#             ),
#             db,
#         )
#         if not res:
#             raise HTTPException(
#                 status_code=status.HTTP_400_BAD_REQUEST,
#                 detail="Co-Link Prev Failed",
#             )

#     if payload.next_recording_id is not None:
#         res = coLinkRecs(
#             schemas.CoLinkRecording(
#                 id=payload.next_recording_id, prev_recording_id=payload.id
#             ),
#             db,
#         )
#         if not res:
#             raise HTTPException(
#                 status_code=status.HTTP_400_BAD_REQUEST,
#                 detail="Co-Link Next Failed",
#             )

#     return getOneRec(payload.id, db)


# def coLinkRecs(payload: schemas.CoLinkRecording, db: Session):
#     update_data = payload.dict(exclude_unset=True)
#     if update_data != {}:
#         db.query(Recording).filter(Recording.id == payload.id).update(
#             update_data,
#             synchronize_session="fetch",
#         )
#         db.commit()
#     return True


# def updateLink(db: Session, prevID=None, nextID=None) -> bool:
#     if prevID is None and nextID is None:
#         if prevID is None:
#             raise HTTPException(
#                 status_code=status.HTTP_400_BAD_REQUEST,
#                 detail="Should Provide prev or next",
#             )
#     if prevID:
#         db.query(Recording).filter(Recording.id == prevID).update(
#             {"next_recording_id": None},
#             synchronize_session="fetch",
#         )
#         db.commit()
#     if nextID:
#         db.query(Recording).filter(Recording.id == nextID).update(
#             {"prev_recording_id": None},
#             synchronize_session="fetch",
#         )
#         db.commit()
#     return True
