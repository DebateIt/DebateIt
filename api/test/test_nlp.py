from fastapi.testclient import TestClient
from ..main import app
from ..database import SessionLocal
import pytest
from .. import crud
from ..auth import verify_password


client = TestClient(app)


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


def test_get_topics():
    topics = crud.getAllTopics(SessionLocal())
    assert topics is not []


def test_sentence_sim():
    res = client.post(
        "/nlp/sentence_sim",
        json={"new_topic": "Do you like feminism form in your country?"},
    )
    assert res.status_code is 200
    assert res.json() is None

    res1 = client.post(
        "/nlp/sentence_sim",
        json={"new_topic": "Do you think feminism works for women?"},
    )
    assert res1.json() == "Is feminism about female dominance?"
