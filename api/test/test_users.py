from glob import glob
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

def test_create_user():
    res = client.post("/user",json={"username":"Simon002","password":"002"})
    assert verify_password("002",res.json().get("password")) is True
    assert res.status_code == 201

def test_login():
    res = client.post("/login",json={"username":"Simon002","password":"002"})
    global token
    token = res.json().get('token_content')
    assert res.status_code == 200

def test_update_user():
    global token
    res = client.put("/user",json={"new_username":"Simon002New","password":"002New"},\
        headers={"Authorization":"Bearer "+token})
    token = res.json().get('token_content')
    assert res.status_code == 200

def test_del_user():
    global token
    res = client.delete("/user", headers={"Authorization":"Bearer "+token})
    assert res.status_code == 200
