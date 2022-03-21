from fastapi.testclient import TestClient
from ..main import app
from ..database import SessionLocal
import pytest
from ..auth import verify_password


client = TestClient(app)
global token
global creator_id
global topic_id


# Topic related tests
@pytest.fixture()
def init_db():
    client.get("/utils/seed")

    # Create an user for later topic testing
    res = client.post("/user", json={"username": "TestUser", "password": "666"})
    global creator_id
    creator_id = int(res.json().get("id"))

    # Retrieve token for later CRUD operations
    res = client.post("/login", json={"username": "TestUser", "password": "666"})
    global token
    token = res.json().get("token_content")


# def test_create_topic(init_db):
def test_create_topic(init_db):
    # Create a topic
    res = client.post(
        "/topic",
        json={"name": "TestTopic1", "description": "a dummy testing topic",
              "creator_id": creator_id, "num_of_debates": 168},
        headers={"Authorization": "Bearer " + token},
    )
    assert res.status_code == 201 # check status code

    global topic_id
    topic_id = int(res.json().get("id"))

    # pass an existed name (use a topic created in the crud seed api)
    res = client.post(
        "/topic",
        json={"name": "Should we ban racial slur on social media?", "description": "a dummy testing topic",
              "creator_id": creator_id, "num_of_debates": 168},
        headers={"Authorization": "Bearer " + token},
    )
    assert res.status_code == 400  # check status code
    assert res.json().get("detail") == "Topic Name Already Exist"

    # pass a JSON body without name
    res = client.post(
        "/topic",
        json={"description": "a dummy testing topic",
              "creator_id": creator_id, "num_of_debates": 168},
        headers={"Authorization": "Bearer " + token},
    )
    assert res.status_code == 422  # check status code
    assert res.json().get("detail")[0]["loc"] == ["body", "name"]
    assert res.json().get("detail")[0]["msg"] == "field required"

    # pass a JSON body without creator_id
    res = client.post(
        "/topic",
        json={"name": "TestTopic2", "description": "a dummy testing topic",
              "num_of_debates": 168},
        headers={"Authorization": "Bearer " + token},
    )
    assert res.status_code == 201  # check status code

    # pass a JSON body with a creator id that is not existed
    res = client.post(
        "/topic",
        json={"name": "TestTopic3", "description": "a dummy testing topic",
              "creator_id": -1, "num_of_debates": 168},
        headers={"Authorization": "Bearer " + token},
    )
    assert res.status_code == 201  # check status code

    # pass num_of_debates with a negative number
    res = client.post(
        "/topic",
        json={"name": "TestTopic4", "description": "a dummy testing topic",
              "creator_id": creator_id, "num_of_debates": -1},
        headers={"Authorization": "Bearer " + token},
    )
    assert res.status_code == 422  # check status code
    assert res.json().get("detail")[0]["loc"] == ["body", "num_of_debates"]
    assert res.json().get("detail")[0]["msg"] == "ensure this value is greater than or equal to 0"


def test_read_topic():
    # Read the newly created topic
    res = client.get(
        "/topic/"+str(topic_id),
        headers={"Authorization": "Bearer " + token},
    )
    assert res.status_code == 200  # check status code

    # Read a topic that doesn't exist
    res = client.get(
        "/topic/0",
        headers={"Authorization": "Bearer " + token},
    )
    assert res.status_code == 404  # check status code
    assert res.json().get("detail") == "Topic Not Found"

    # Pass a URL param without topic id
    res = client.get(
        "/topic/",
        headers={"Authorization": "Bearer " + token},
    )
    assert res.status_code == 405  # check status code


def test_update_topic():
    # Update the newly created topic
    res = client.put(
        "/topic/"+str(topic_id),
        json={"name": "TestTopic1", "description": "topic is updated",
              "creator_id": creator_id, "num_of_debates": 16888888},
        headers={"Authorization": "Bearer " + token},
    )
    assert res.status_code == 200  # check status code

    # Pass a JSON body without name
    res = client.put(
        "/topic/" + str(topic_id),
        json={"description": "topic is updated",
              "creator_id": creator_id, "num_of_debates": 16888888},
        headers={"Authorization": "Bearer " + token},
    )
    assert res.status_code == 200  # check status code

    # Pass a JSON body without description
    res = client.put(
        "/topic/" + str(topic_id),
        json={"name": "TestTopic1",
              "creator_id": creator_id, "num_of_debates": 16888888},
        headers={"Authorization": "Bearer " + token},
    )
    assert res.status_code == 200  # check status code

    # Pass a JSON body without creator id
    res = client.put(
        "/topic/" + str(topic_id),
        json={"name": "TestTopic1", "description": "topic is updated",
              "num_of_debates": 16888888},
        headers={"Authorization": "Bearer " + token},
    )
    assert res.status_code == 200  # check status code

    # Pass a JSON body without the number of debates
    res = client.put(
        "/topic/" + str(topic_id),
        json={"name": "TestTopic1", "description": "topic is updated",
              "creator_id": creator_id},
        headers={"Authorization": "Bearer " + token},
    )
    assert res.status_code == 200  # check status code

    # Update a topic that doesn't exist
    res = client.put(
        "/topic/0",
        json={"name": "TestTopic1", "description": "topic is updated",
              "creator_id": creator_id, "num_of_debates": 16888888},
        headers={"Authorization": "Bearer " + token},
    )
    assert res.status_code == 404  # check status code
    assert res.json().get("detail") == "Topic Not Found"

    # Pass a URL param without topic id
    res = client.put(
        "/topic/",
        json={"name": "TestTopic1", "description": "topic is updated",
              "creator_id": creator_id, "num_of_debates": 16888888},
        headers={"Authorization": "Bearer " + token},
    )
    assert res.status_code == 307  # check status code

    # Pass a JSON body with the old topic name
    res = client.put(
        "/topic/" + str(topic_id),
        json={"name": "TestTopic1", "description": "topic is updated",
              "creator_id": creator_id, "num_of_debates": 16888888},
        headers={"Authorization": "Bearer " + token},
    )
    assert res.status_code == 200  # check status code

    # Pass a JSON body with an existing topic name
    res = client.put(
        "/topic/" + str(topic_id),
        json={"name": "Should we ban racial slur on social media?", "description": "topic is updated",
              "creator_id": creator_id, "num_of_debates": 16888888},
        headers={"Authorization": "Bearer " + token},
    )
    assert res.status_code == 400  # check status code
    assert res.json().get("detail") == "Topic Name Already Exist"


def test_delete_topic():
    # Delete the newly created topic
    res = client.delete(
        "/topic/" + str(topic_id),
        headers={"Authorization": "Bearer " + token},
    )
    assert res.status_code == 200  # check status code

    # Delete a topic that is not existed
    res = client.delete(
        "/topic/" + str(topic_id),
        headers={"Authorization": "Bearer " + token},
    )
    assert res.status_code == 404  # check status code
    assert res.json().get("detail") == "Topic Not Found"

    # Reseed all tables
    client.get("/utils/seed")
