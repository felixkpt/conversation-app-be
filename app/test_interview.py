# test_interview.py

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_conduct_interview():
    sub_cat_id = 1
    user_id = 1

    response = client.post(f"/interview/{sub_cat_id}/{user_id}")
    assert response.status_code == 200
    assert response.json() == {"message": "Interview completed successfully"}
