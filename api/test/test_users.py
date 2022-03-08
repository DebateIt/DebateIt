from fastapi.testclient import TestClient
from ..main import app
from ..database import SessionLocal
import pytest
from ..auth import verify_password

client = TestClient(app)
global token


@pytest.fixture()
def init_db():
    client.get("/utils/seed")


def test_get_info(init_db):
    res = client.get("/user/Alice")
    assert verify_password("alice", res.json().get("password")) is True
    assert res.status_code == 200

    # Pass a username that doesn't exist
    res_err = client.get("/user/Alice2")
    assert res_err.status_code == 404


def test_create_user():
    res = client.post("/user", json={"username": "Simon002", "password": "002"})
    assert verify_password("002", res.json().get("password")) is True
    assert res.status_code == 201

    # Pass a username that conflicts with an existing one
    res1 = client.post("/user", json={"username": "Alice", "password": "002"})
    assert res1.status_code == 400
    assert res1.json().get("detail") == "Username Already Exist"

    # Pass a JSON body without a username field
    res2 = client.post("/user", json={"password": "002"})
    assert res2.status_code == 422
    assert res2.json().get("detail")[0]["loc"] == ["body", "username"]
    assert res2.json().get("detail")[0]["msg"] == "field required"

    # Pass a JSON body without a password field
    res3 = client.post("/user", json={"username": "002"})
    assert res3.status_code == 422
    assert res3.json().get("detail")[0]["loc"] == ["body", "password"]
    assert res3.json().get("detail")[0]["msg"] == "field required"


def test_login():
    res = client.post("/login", json={"username": "Simon002", "password": "002"})
    global token
    token = res.json().get("token_content")
    assert res.status_code == 200

    # Pass a username that doesn't exist
    res1 = client.post("/login", json={"username": "Simon", "password": "002"})
    assert res1.json().get("detail") == "Invalid Username or Password"
    assert res1.status_code == 400

    # Pass a JSON body without a username field
    res2 = client.post("/user", json={"password": "002"})
    assert res2.status_code == 422
    assert res2.json().get("detail")[0]["loc"] == ["body", "username"]
    assert res2.json().get("detail")[0]["msg"] == "field required"

    # Pass a JSON body with a wrong password
    res3 = client.post("/user", json={"username": "002"})
    assert res3.status_code == 422
    assert res3.json().get("detail")[0]["loc"] == ["body", "password"]
    assert res3.json().get("detail")[0]["msg"] == "field required"


def test_update_user():
    global token
    res = client.put(
        "/user",
        json={"username": "Simon002New", "password": "002New"},
        headers={"Authorization": "Bearer " + token},
    )
    token = res.json().get("token_content")
    assert res.status_code == 200

    # Pass a username that conflicts with an existing one
    res1 = client.put(
        "/user",
        json={"username": "Alice", "password": "Conflicts"},
        headers={"Authorization": "Bearer " + token},
    )
    assert res1.status_code == 400
    assert res1.json().get("detail") == "Username Already Exist"

    # Send the request without providing a token
    res2 = client.put(
        "/user", json={"username": "Alice", "password": "Conflicts"}
    )
    assert res2.status_code == 401
    assert res2.json().get("detail") == "Not authenticated"

    # Pass new_username with the current username
    res3 = client.put(
        "/user",
        json={"username": "Simon002New", "password": "002New"},
        headers={"Authorization": "Bearer " + token},
    )
    assert res3.status_code == 400
    assert res3.json().get("detail") == "Username Already Exist"

    # Pass a JSON body without new_username field
    res4 = client.put(
        "/user",
        json={"password": "002NewNew"},
        headers={"Authorization": "Bearer " + token},
    )
    token = res4.json().get("token_content")
    assert res.status_code == 200

    # Pass a JSON body without password field
    res5 = client.put(
        "/user",
        json={"username": "Simon002NewNew"},
        headers={"Authorization": "Bearer " + token},
    )
    token = res5.json().get("token_content")
    assert res.status_code == 200

    # Send the request without a JSON body
    res6 = client.put("/user", json={}, headers={"Authorization": "Bearer " + token})
    token = res5.json().get("token_content")
    assert res.status_code == 200


def test_del_user():
    global token
    res = client.delete("/user", headers={"Authorization": "Bearer " + token})
    assert res.status_code == 200

    # Send the request without a token
    res2 = client.delete("/user")
    assert res2.status_code == 401
    assert res2.json().get("detail") == "Not authenticated"
