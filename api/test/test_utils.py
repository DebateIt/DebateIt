from fastapi.testclient import TestClient

from ..main import app
from ..database import SessionLocal
from ..models import *

client = TestClient(app)

def test_seed():
    db = SessionLocal()

    response = client.get("/utils/seed")
    assert response.status_code == 200
    assert response.json() == {
        "msg": "Success!"
    }
    assert db.query(User).count() == 3
    assert db.query(Topic).count() == 3
