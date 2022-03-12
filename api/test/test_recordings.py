from pydoc import cli
from fastapi.testclient import TestClient
from ..main import app
from ..database import SessionLocal
import pytest
from ..auth import verify_password
from .. import crud

client = TestClient(app)

global tokenAlice
global tokenBob
global tokenAdmin
global debateID
global debateID2
global aliceID
global bobID
global evaID
global adminID
global topicID
global topicID2
global recID1
global recID2
global recID3
global recID4


def helper(res):
    print(res)
    print(res.json())

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
    global tokenAlice
    tokenAlice = resA.json().get("token_content")
    assert resA.status_code == 200

    resB = client.post("/login", json={"username": "Bob", "password": "bob"})
    global tokenBob
    tokenBob = resB.json().get("token_content")
    assert resB.status_code == 200

    resAdmin = client.post("/login", json={"username": "Admin", "password": "admin"})
    global tokenAdmin
    tokenAdmin = resAdmin.json().get("token_content")
    assert resAdmin.status_code == 200


def test_globals():
    global tokenAlice
    global tokenBob
    global tokenAdmin
    global debateID
    global debateID2
    global aliceID
    global bobID
    global evaID
    global adminID
    global topicID
    global topicID2

    alice = client.get("/user/Alice")
    aliceID = alice.json().get("id")
    bob = client.get("/user/Bob")
    bobID = bob.json().get("id")
    admin = client.get("/user/Admin")
    adminID = admin.json().get("id")
    eva = client.get("/user/Eva")
    evaID = eva.json().get("id")

    assert aliceID is not None
    assert bobID is not None
    assert adminID is not None
    assert evaID is not None

    topic1 = crud.getOneTopicByName(
        "Should we ban racial slur on social media?", db=SessionLocal()
    )
    topic2 = crud.getOneTopicByName(
        "Will there be a war between US and China?", db=SessionLocal()
    )
    topicID = topic1.id
    topicID2 = topic2.id

    
    assert topicID is not None
    assert topicID2 is not None

    debate1 = crud.getOneDebateByTopicId(topicID,db=SessionLocal())
    debate2 = crud.getOneDebateByTopicId(topicID2,db=SessionLocal())
    debateID = debate1.id
    debateID2 = debate2.id

    assert debateID is not None
    assert debateID2 is not None
    
def test_add_rec():
    global recID1
    global recID2
    global recID3
    global recID4
    res = client.post("/recording",
        json={"debate_id":debateID,"user_id":aliceID,"audio_content":"the first sentence."},
        headers={"Authorization": "Bearer " + tokenAdmin})
    assert res.status_code == 201
    recID1 = res.json().get("id")
    assert recID1 is not None
    assert res.json().get("user_id") == aliceID
    assert res.json().get("debate_id") == debateID
    assert res.json().get("audio_content") == "the first sentence."
    assert res.json().get("prev_recording_id") is None
    assert res.json().get("next_recording_id") is None
    
    res1 = client.post("/recording",
        json={"debate_id":0,"user_id":aliceID,"audio_content":"the first sentence."},
        headers={"Authorization": "Bearer " + tokenAdmin})
    assert res1.status_code == 400
    assert res1.json().get("detail") == 'Debate Not Exist'

    res2 = client.post("/recording",
        json={"debate_id":debateID,"user_id":0,"audio_content":"the first sentence."},
        headers={"Authorization": "Bearer " + tokenAdmin})
    assert res2.status_code == 400
    assert res2.json().get("detail") == 'User Not Exist'

    res3 = client.post("/recording",
        json={"debate_id":debateID,"user_id":aliceID,"audio_content":None},
        headers={"Authorization": "Bearer " + tokenAdmin})
    assert res3.status_code == 422

    res4 = client.post("/recording",
        json={"debate_id":debateID,"user_id":aliceID,"audio_content":"the first sentence."},
        headers={"Authorization": "Bearer " + tokenAlice})
    assert res4.status_code == 401
    assert res4.json().get("detail") == 'Only Admin can add debate'

    res41 = client.post("/recording",
        json={"debate_id":debateID,"user_id":evaID,"audio_content":"the first sentence."},
        headers={"Authorization": "Bearer " + tokenAdmin})
    assert res41.status_code == 400
    assert res41.json().get("detail") == "User Not In This Debate"

    # These are recordings prepared for next section
    res5 = client.post("/recording",
        json={"debate_id":debateID,"user_id":bobID,"audio_content":"the second sentence."},
        headers={"Authorization": "Bearer " + tokenAdmin})
    
    res6 = client.post("/recording",
        json={"debate_id":debateID,"user_id":aliceID,"audio_content":"the third sentence."},
        headers={"Authorization": "Bearer " + tokenAdmin})
    
    res7 = client.post("/recording",
        json={"debate_id":debateID2,"user_id":bobID,"audio_content":"the unrelated sentence."},
        headers={"Authorization": "Bearer " + tokenAdmin})

    assert res5.status_code == 201
    assert res6.status_code == 201
    assert res7.status_code == 201
    recID2 = res5.json().get("id")
    recID3 = res6.json().get("id")
    recID4 = res7.json().get("id")

    
def test_link_rec():
    # rec2 <-> rec1 <-> rec3
    res = client.post("/recording/link",
        json={"id":recID1,"prev_recording_id":recID2},
        headers={"Authorization": "Bearer " + tokenAdmin})
    assert res.status_code == 200
    assert res.json().get("prev_recording_id") == recID2

    thePrev = client.get(f"/recording/{recID2}")
    assert thePrev.json().get("next_recording_id") == recID1

    res2 = client.post("/recording/link",
        json={"id":recID1,"prev_recording_id":recID3},
        headers={"Authorization": "Bearer " + tokenAdmin})
    assert res2.status_code == 400
    assert res2.json().get("detail") == 'Prev Position Unavailable, use Update instead'
    
    res3 = client.post("/recording/link",
        json={"id":recID1,"next_recording_id":recID3},
        headers={"Authorization": "Bearer " + tokenAlice})
    assert res3.status_code == 401
    assert res3.json().get("detail") == 'Only Admin can link debate'

    res4 = client.post("/recording/link",
        json={"id":recID1,"next_recording_id":recID4},
        headers={"Authorization": "Bearer " + tokenAdmin})
    assert res4.status_code == 400
    assert res4.json().get("detail") == 'Next and Current Recordings Have Different Debate ID'
    
    res5 = client.post("/recording/link",
        json={"id":recID1,"next_recording_id":recID3},
        headers={"Authorization": "Bearer " + tokenAdmin})
    assert res5.status_code == 200
    assert res5.json().get("next_recording_id") == recID3

    theNext = client.get(f"/recording/{recID3}")
    assert theNext.json().get("prev_recording_id") == recID1

def test_del_rec():
    res = client.delete(f"/recording/{recID3}", headers={"Authorization": "Bearer " + tokenAdmin})
    assert res.status_code == 200
    
    thePrev = client.get(f"/recording/{recID1}")
    assert thePrev.json().get("next_recording_id") is None
    
    # 删除中间的需要额外的提醒吗
