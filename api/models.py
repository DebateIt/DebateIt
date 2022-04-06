from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Text,
    Enum,
    DateTime,
    LargeBinary,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from .database import Base


class Status(enum.Enum):
    BeforeDebate = 1
    InProgress = 2
    End = 3
    Finish = 4

    # End is when debate ends, one party has left
    # finish is when both left
    # when changing the Type, old type in the database need to be droped


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    password = Column(String, nullable=False)


class Topic(Base):
    __tablename__ = "topics"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    description = Column(Text, default="")
    num_of_debates = Column(Integer, default=0)

    creator_id = Column(Integer, ForeignKey("users.id"), nullable=False)


class Debate(Base):
    __tablename__ = "debates"

    id = Column(Integer, primary_key=True, index=True)
    nth_time_of_debate = Column(Integer, nullable=False)
    start_time = Column(DateTime(timezone=True), server_default=func.now())
    status = Column(Enum(Status), default=Status.BeforeDebate)
    topic_id = Column(Integer, ForeignKey("topics.id"), nullable=False)
    pro_user_id = Column(Integer, ForeignKey("users.id"))
    con_user_id = Column(Integer, ForeignKey("users.id"))


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String)

    debate_id = Column(Integer, ForeignKey("debates.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
