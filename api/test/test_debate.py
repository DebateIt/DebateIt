from fastapi.testclient import TestClient
from ..main import app
from ..database import SessionLocal
import pytest
from ..auth import verify_password
from .. import crud

client = TestClient(app)
global token1
global token2
global debateID
global debateID2
global aliceID
global bobID
global topicID
global topicID2


def helper(res):
    print(res)
    print(res.json())


@pytest.fixture()
def init_db():
    client.get("/utils/seed")


def test_get_token(init_db):
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
        json={"topic_id": topicID, "as_pro": True, "start_time": "2022-03-16T12:20:00"},
        headers={"Authorization": "Bearer " + token1},
    )
    debateID = res.json().get("id")
    assert debateID is not None
    assert res.json().get("nth_time_of_debate") is 1
    assert res.json().get("topic_id") is topicID
    assert res.json().get("pro_user_id") == aliceID
    assert res.json().get("con_user_id") is None
    assert res.json().get("first_recording_id") is None
    assert res.json().get("last_recording_id") is None
    assert res.json().get("status") is 1

    res11 = client.post(
        "/debate",
        json={
            "topic_id": topicID2,
            "as_pro": True,
            "start_time": "2022-03-17T12:20:00",
        },
        headers={"Authorization": "Bearer " + token1},
    )
    debateID2 = res11.json().get("id")

    res2 = client.post(
        "/debate",
        json={"topic_id": 0, "as_pro": True, "start_time": "2022-03-16T12:20:00"},
        headers={"Authorization": "Bearer " + token1},
    )
    assert res2.status_code == 400
    assert res2.json().get("detail") == "Topic Not Exist"

    res3 = client.post(
        "/debate",
        json={"topic_id": topicID, "start_time": "2022-03-16T12:20:00"},
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
            "start_time": "2022-03-16T12:20:00",
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
            "start_time": "2022-03-16T12:20:00",
        },
        headers={"Authorization": "Bearer " + token1},
    )
    assert res31.status_code == 400
    assert res31.json().get("detail") == "Both Pro and Con are None"

    res4 = client.post(
        "/debate",
        json={"topic_id": topicID, "as_pro": True, "start_time": "2021-03-16T12:20:00"},
        headers={"Authorization": "Bearer " + token1},
    )
    assert res4.status_code == 400
    assert res4.json().get("detail") == "Start Time Need to Be Later"

    res5 = client.post(
        "/debate",
        json={"topic_id": topicID, "as_pro": True, "start_time": "2021-03-16T12:20:00"},
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