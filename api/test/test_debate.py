from random import randint
from fastapi.testclient import TestClient
from ..main import app
from ..database import SessionLocal
import pytest
from ..auth import verify_password
from .. import crud
from datetime import datetime, timedelta

client = TestClient(app)
global token1
global token2
global debateID
global debateID2
global aliceID
global bobID
global topicID
global topicID2

global startTime
now = datetime.now() + timedelta(
    days=randint(1, 5),
    minutes=randint(1, 38),
    hours=randint(1, 53),
    seconds=randint(2, 45),
)
startTime = datetime.strftime(now, "%Y-%m-%dT%H:%M:%S")


@pytest.fixture()
def init_db():
    client.get("/utils/seed")


def test_init(init_db):
    res = client.get("/user/Alice")
    assert verify_password("alice", res.json().get("password")) is True
    assert res.status_code == 200

    # Pass a username that doesn't exist
    res_err = client.get("/user/Alice2")
    assert res_err.status_code == 404


def test_login():
    # Just get tokens from users, no need to test exceptions
    resA = client.post("/login", json={"username": "Alice", "password": "alice"})
    global token1
    token1 = resA.json().get("token_content")
    assert resA.status_code == 200

    resB = client.post("/login", json={"username": "Bob", "password": "bob"})
    global token2
    token2 = resB.json().get("token_content")
    assert resB.status_code == 200


def test_add_debate():
    global token1
    global debateID
    global debateID2
    global aliceID
    global bobID
    global topicID
    global topicID2

    alice = client.get("/user/Alice")
    aliceID = alice.json().get("id")
    bob = client.get("/user/Bob")
    bobID = bob.json().get("id")
    topic1 = crud.getOneTopicByName(
        "Should we ban racial slur on social media?", db=SessionLocal()
    )
    topic2 = crud.getOneTopicByName(
        "Will there be a war between US and China?", db=SessionLocal()
    )
    topicID = topic1.id
    topicID2 = topic2.id

    assert aliceID is not None
    assert topicID is not None
    assert topicID2 is not None

    res = client.post(
        "/debate",
        json={"topic_id": topicID, "as_pro": True, "start_time": startTime},
        headers={"Authorization": "Bearer " + token1},
    )
    assert res.status_code == 201
    debateID = res.json().get("id")
    assert debateID is not None
    assert res.json().get("nth_time_of_debate") == 1
    assert res.json().get("topic_id") == topicID
    assert res.json().get("pro_user_id") == aliceID
    assert res.json().get("con_user_id") is None
    assert res.json().get("first_recording_id") is None
    assert res.json().get("last_recording_id") is None
    assert res.json().get("status") == 1

    res11 = client.post(
        "/debate",
        json={
            "topic_id": topicID2,
            "as_pro": True,
            "start_time": startTime,
        },
        headers={"Authorization": "Bearer " + token1},
    )
    debateID2 = res11.json().get("id")

    res2 = client.post(
        "/debate",
        json={"topic_id": 0, "as_pro": True, "start_time": startTime},
        headers={"Authorization": "Bearer " + token1},
    )
    assert res2.status_code == 400
    assert res2.json().get("detail") == "Topic Not Exist"

    res3 = client.post(
        "/debate",
        json={"topic_id": topicID, "start_time": startTime},
        headers={"Authorization": "Bearer " + token1},
    )
    assert res3.status_code == 400
    assert res3.json().get("detail") == "Both Pro and Con are None"

    res30 = client.post(
        "/debate",
        json={
            "topic_id": topicID,
            "as_pro": True,
            "as_con": True,
            "start_time": startTime,
        },
        headers={"Authorization": "Bearer " + token1},
    )
    assert res30.status_code == 400
    assert res30.json().get("detail") == "Both Pro and Con Entered"

    res31 = client.post(
        "/debate",
        json={
            "topic_id": topicID,
            "as_pros": True,
            "start_time": startTime,
        },
        headers={"Authorization": "Bearer " + token1},
    )
    assert res31.status_code == 400
    assert res31.json().get("detail") == "Both Pro and Con are None"

    res4 = client.post(
        "/debate",
        json={"topic_id": topicID, "as_pro": True, "start_time": "2022-02-02T12:03:00"},
        headers={"Authorization": "Bearer " + token1},
    )
    assert res4.status_code == 400
    assert res4.json().get("detail") == "Start Time Need to Be Later"

    res5 = client.post(
        "/debate",
        json={"topic_id": topicID, "as_pro": True, "start_time": startTime},
        headers={"Authorization": "Bearer "},
    )
    assert res5.status_code == 401
    assert res5.json().get("detail") == "Invalid Credentials"


def test_join_debate():
    global token2
    global debateID
    global debateID2
    global bobID

    res = client.post(
        "/debate/join",
        json={"id": debateID, "as_con": True},
        headers={"Authorization": "Bearer " + token2},
    )
    assert res.status_code == 200
    assert res.json().get("con_user_id") == bobID
    assert res.json().get("status") == 2

    res2 = client.post(
        "/debate/join",
        json={"id": debateID2},
        headers={"Authorization": "Bearer " + token2},
    )
    assert res2.status_code == 400
    assert res2.json().get("detail") == "Pro and Con Cannot be None at same time"

    res3 = client.post(
        "/debate/join",
        json={"id": debateID2, "as_pro": True},
        headers={"Authorization": "Bearer " + token2},
    )
    assert res3.status_code == 400
    assert res3.json().get("detail") == "Pro Position Unavailable"

    res4 = client.post(
        "/debate/join",
        json={"id": debateID2, "as_con": True},
        headers={"Authorization": "Bearer " + token1},
    )
    assert res4.status_code == 400
    assert res4.json().get("detail") == "Cannot take both sides of Debate"

    res5 = client.post(
        "/debate/join",
        json={"id": debateID2, "as_con": True},
        headers={"Authorization": "Bearer "},
    )
    assert res5.status_code == 401
    assert res5.json().get("detail") == "Invalid Credentials"

    res6 = client.post(
        "/debate/join",
        json={"id": 0, "as_con": True},
        headers={"Authorization": "Bearer " + token2},
    )
    assert res6.status_code == 400
    assert res6.json().get("detail") == "Debate Not Exist"

    res7 = client.post(
        "/debate/join",
        json={"id": debateID, "as_con": True},
        headers={"Authorization": "Bearer " + token2},
    )
    assert res7.status_code == 400
    assert res7.json().get("detail") == "Wrong Debate Status, Cannot Join Now"

def test_message():
    global debateID
    global aliceID
    res = client.get(f"/room/initialize/{debateID}")
    assert res.json().get("pro_turn") is True
    assert res.json().get("debate_id") == debateID

    res2 = client.post("/room/message",
        json={"content":"I hope this to be true","debate_id":debateID,"pro_turn":True},
        headers={"Authorization": "Bearer " + token1})

    assert res2.json().get("pro_turn") is False

    res3 = client.post("/room/message",
        json={"content":"I hope this to be true again","debate_id":debateID,"pro_turn":True},
        headers={"Authorization": "Bearer " + token1})
    assert res3.status_code == 400
    assert res3.json().get("detail") == 'Turn Match Error'

    res4 = client.post("/room/message",
        json={"content":"I hope this to be true again","debate_id":debateID,"pro_turn":False},
        headers={"Authorization": "Bearer " + token1})
    assert res4.status_code == 400
    assert res4.json().get("detail") == f'User #{aliceID} cannot send message in this turn!'

    res5 = client.post("/room/message",
        json={"content":"I hope this to be true again","debate_id":debateID,"pro_turn":False},
        headers={"Authorization": "Bearer "})
    assert res5.status_code == 401
    assert res5.json().get("detail") ==  'Invalid Credentials'

    res6 = client.post("/room/message",
        json={"content":"I don't like this","debate_id":debateID,"pro_turn":False},
        headers={"Authorization": "Bearer "+token2})
    print(res6.json())


def test_leave_debate():
    global token1
    global token2
    global debateID
    global debateID2

    res = client.post(
        "debate/exit",
        json={"id": debateID, "as_con": True},
        headers={"Authorization": "Bearer " + token2},
    )
    assert res.status_code == 200
    assert res.json().get("con_user_id") is None
    assert res.json().get("status") == 3

    res2 = client.post(
        "/debate/join",
        json={"id": debateID, "as_con": True},
        headers={"Authorization": "Bearer " + token2},
    )
    assert res2.status_code == 400
    assert res2.json().get("detail") == "Wrong Debate Status, Cannot Join Now"

    res3 = client.post(
        "/debate/exit",
        json={"id": debateID, "as_pro": True},
        headers={"Authorization": "Bearer " + token2},
    )
    assert res3.status_code == 400
    assert res3.json().get("detail") == "Pro User Doesn't Match"

    res4 = client.post(
        "/debate/exit",
        json={"id": debateID, "as_pro": True},
        headers={"Authorization": "Bearer " + token1},
    )
    assert res4.status_code == 200
    assert res4.json().get("status") == 4
    assert res4.json().get("con_user_id") is None

    res5 = client.post(
        "/debate/join",
        json={"id": debateID, "as_con": True},
        headers={"Authorization": "Bearer " + token2},
    )
    assert res5.status_code == 400
    assert res5.json().get("detail") == "Wrong Debate Status, Cannot Join Now"

    res6 = client.post(
        "/debate/exit",
        json={"id": debateID2, "as_pro": True},
        headers={"Authorization": "Bearer " + token1},
    )
    assert res6.status_code == 200
    assert res6.json() is True

    # In this test I didn't write anything about deleting a debate & update debate.
    # Might leave it to the refactoring.
    # Also In the previous tests some uses delete&update.
    # because I'm still not sure on how it will be used externally (as API)
