from sqlalchemy import delete
from sqlalchemy.orm import Session
from .models import *

def seed(db: Session) -> None:
    # Empty the database
    tables = [User, Topic, Debate, Recording]
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
