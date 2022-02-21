from glob import glob
from tracemalloc import reset_peak
from fastapi.testclient import TestClient
from fastapi import Depends, status, HTTPException
from sqlalchemy.orm import Session
from ..dependencies import get_db
from ..main import app
from ..database import SessionLocal
import pytest
from ..crud import clean_up_user_table
from ..auth import verify_password

client = TestClient(app)
global token

def test_get_info():
    res = client.get("/user/Alice")
    assert res.json().get("password") == "12345"
    assert res.status_code == 200
    res_err = client.get("/user/Alice2")
    assert res_err.status_code == 404

def test_create_user():
    res = client.post("/user",json={"username":"Simon002","password":"002"})
    assert verify_password("002",res.json().get("password")) is True
    assert res.status_code == 201

    res1 = client.post("/user",json={"username":"Alice","password":"002"})
    assert res1.status_code == 400
    assert res1.json().get("detail") == 'Username Already Exist'

    res2 = client.post("/user",json={"password":"002"})
    assert res2.status_code == 422
    assert res2.json().get("detail")[0]["loc"] == ['body','username']
    assert res2.json().get("detail")[0]["msg"] == 'field required'

    res3 = client.post("/user",json={"username":"002"})
    assert res3.status_code == 422
    assert res3.json().get("detail")[0]["loc"] == ['body','password']
    assert res3.json().get("detail")[0]["msg"] == 'field required'

def test_login():
    res = client.post("/login",json={"username":"Simon002","password":"002"})
    global token
    token = res.json().get('token_content')
    assert res.status_code == 200

    res1 = client.post("/login",json={"username":"Simon","password":"002"})
    assert res1.json().get("detail") == 'Username Not Exist'
    assert res1.status_code == 400

    res2 = client.post("/user",json={"password":"002"})
    assert res2.status_code == 422
    assert res2.json().get("detail")[0]["loc"] == ['body','username']
    assert res2.json().get("detail")[0]["msg"] == 'field required'

    res3 = client.post("/user",json={"username":"002"})
    assert res3.status_code == 422
    assert res3.json().get("detail")[0]["loc"] == ['body','password']
    assert res3.json().get("detail")[0]["msg"] == 'field required'

def test_update_user():
    global token
    res = client.put("/user",json={"new_username":"Simon002New","new_password":"002New"},\
        headers={"Authorization":"Bearer "+token})
    token = res.json().get('token_content')
    assert res.status_code == 200

    res1 = client.put("/user",json={"new_username":"Alice","new_password":"Conflicts"},\
        headers={"Authorization":"Bearer "+token})
    assert res1.status_code == 400
    assert res1.json().get("detail") == 'Username Already Exist'

    res2 = client.put("/user",json={"new_username":"Alice","new_password":"Conflicts"})
    assert res2.status_code == 401
    assert res2.json().get("detail") == 'Not authenticated'

    res3 = client.put("/user",json={"new_username":"Simon002New","new_password":"002New"},\
        headers={"Authorization":"Bearer "+token})
    assert res3.status_code == 400
    assert res3.json().get("detail") == 'Username Already Exist'

    res4 = client.put("/user",json={"new_password":"002NewNew"},headers={"Authorization":"Bearer "+token})
    token = res4.json().get('token_content')
    assert res.status_code == 200

    res5 = client.put("/user",json={"new_username":"Simon002NewNew"},headers={"Authorization":"Bearer "+token})
    token = res5.json().get('token_content')
    assert res.status_code == 200

    res6 = client.put("/user",json = {},headers={"Authorization":"Bearer "+token})
    token = res5.json().get('token_content')
    assert res.status_code == 200

def test_del_user():
    global token
    res = client.delete("/user", headers={"Authorization":"Bearer "+token})
    assert res.status_code == 200

    res2 = client.delete("/user")
    assert res2.status_code == 401
    assert res2.json().get("detail") == 'Not authenticated'