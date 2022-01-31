from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime, LargeBinary
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .database import Base

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

    topic_id = Column(Integer, ForeignKey("topics.id"), nullable=False)
    pro_user_id = Column(Integer, ForeignKey("users.id"))
    con_user_id = Column(Integer, ForeignKey("users.id"))
    first_recording_id = Column(Integer, ForeignKey("recordings.id"))
    last_recording_id = Column(Integer, ForeignKey("recordings.id"))

class Recording(Base):
    __tablename__ = "recordings"

    id = Column(Integer, primary_key=True, index=True)
    audio_content = Column(LargeBinary)

    debate_id = Column(Integer, ForeignKey("debates.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    prev_recording_id = Column(Integer, ForeignKey("recordings.id"))
    next_recording_id = Column(Integer, ForeignKey("recordings.id"))
