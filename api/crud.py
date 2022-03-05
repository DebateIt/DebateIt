from sqlalchemy import update, delete
from sqlalchemy.orm import Session
from fastapi import status, Response,HTTPException

from .models import *
from . import schemas, auth


def seed(db: Session) -> None:
    # Empty the database
    tables = [Recording, Debate, Topic, User]
    for t in tables:
        db.execute(delete(t))
    db.commit()

    # Create Users
    alice = User(id=1,username="Alice", password=auth.pwd_context.hash("alice"))
    db.add(alice)
    bob = User(id=2,username="Bob", password=auth.pwd_context.hash("bob"))
    db.add(bob)
    eve = User(id=3,username="Eva", password=auth.pwd_context.hash("eva"))
    db.add(eve)
    Admin = User(id=4,username="Admin", password=auth.pwd_context.hash("admin"))
    db.add(Admin)

    db.commit()
    db.refresh(alice)
    db.refresh(bob)
    db.refresh(eve)

    # Create Topics
    slur = Topic(
        id=1,
        name="Should we ban racial slur on social media?",
        description="asdfasdfasdfasfd",
        creator_id=alice.id,
    )
    db.add(slur)
    us_china = Topic(
        id=2,
        name="Will there be a war between US and China?",
        description="asdfasdfasdfasdfasfd",
        creator_id=bob.id,
    )
    db.add(us_china)
    feminism = Topic(
        id=3,
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


# For the return type of this one
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


def IsDebateIdExist(id, db) -> bool:
    res = db.query(Debate).filter(Debate.id == id)
    return db.query(res.exists()).scalar()

def getOneDebate(id, db) -> Debate:
    return db.query(Debate).filter(Debate.id == id).first()


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


def delOneDebate(id, db: Session) -> None:
    db.query(Debate).filter(Debate.id == id).delete(synchronize_session="fetch")
    db.commit()
    return Response(
        status_code=status.HTTP_200_OK, content=f"Debate No.{id} is deleted"
    )


def updateOneDebate(payload: schemas.UpdateDebate, db: Session) -> Debate:
    if payload.new_start_time:
        db.query(Debate).filter(Debate.id == payload.id).update(
        {"start_time": payload.new_start_time},
        synchronize_session="fetch",
        )
    elif payload.new_first_recording_id:
        db.query(Debate).filter(Debate.id == payload.id).update(
        {
            "first_recording_id": payload.new_first_recording_id,
        },
        synchronize_session="fetch",
        )
    elif payload.new_last_recording_id:
        db.query(Debate).filter(Debate.id == payload.id).update(
        {
            "last_recording_id": payload.new_last_recording_id,
        },
        synchronize_session="fetch",
        )
    elif payload.new_status:
        db.query(Debate).filter(Debate.id == payload.id).update(
            {
                "status":payload.new_status
            },
            synchronize_session="fetch",
        )
    db.commit()
    return getOneDebate(payload.id, db)


def userJoinDebate(userID, payload, db) -> Debate:
    # 到这一步，一定是已经一方有人，另一方加入
    # By this point, there must have been someone on one side and the other side joined

    # payload schemas 那里查不出来pro和con是不是一样的，所以需要在这里查一次
    theDebate = getOneDebate(payload.id,db)
    if payload.as_pro and theDebate.con_user_id != userID:
        db.query(Debate).filter(Debate.id == payload.id).update(
            {"pro_user_id": userID}, synchronize_session="fetch"
        )
    elif payload.as_con and theDebate.pro_user_id != userID:
        db.query(Debate).filter(Debate.id == payload.id).update(
            {"con_user_id": userID}, synchronize_session="fetch"
        )
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Cannot take both sides of Debate")

    db.commit()

    #所以这里要更新Debate Status
    updateOneDebate(schemas.UpdateDebate(id=payload.id,new_status=Status.InProgress),db)

    return getOneDebate(payload.id, db)

# 后面要继续改，处理结束debate和离开debate的问题
def userExitDebate(userID, payload, db):
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

    # 这一段整体都很理想化，但是之后可以继续设计
    # This paragraph as a whole are idealized, but after that can continue to design
    if new_deb.status is Status.End:
        # 如果已经是End，那么这就是另一方也离开了这个Debate，不用做什么改变
        # 状态改成Finished就行了
        return updateOneDebate(schemas.UpdateDebate(id=payload.id ,new_status=Status.Finish),db)
    elif new_deb.status is Status.BeforeDebate and\
        new_deb.con_user_id is None and new_deb.pro_user_id is None:
        # 这个对应还没有另一个人进来，创建的那个人就已经走了，那么就直接删除Debate就行
        # This corresponds to the one who has left before another person has come in, so just delete Debate
        return delOneDebate(new_deb.id, db)
    else:
        # 这个对应结束了Debate，有一方先行离开了
        # This corresponds to the end of the Debate, one of the parties left first
        return updateOneDebate(schemas.UpdateDebate(id=payload.id ,new_status=Status.End),db)
