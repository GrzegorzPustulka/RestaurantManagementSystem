from fastapi.testclient import TestClient
from tests.conftest import client, db
from sqlalchemy.orm import Session


def test_login(db: Session, client: TestClient):
    response = client.post(
        "auth", data={"username": "email_0", "password": "password_0"}
    )
    assert response.status_code == 200
    assert response.json()["access_token"]
    assert response.json()["token_type"] == "bearer"


def test_login_fail(db: Session, client: TestClient):
    response = client.post(
        "auth", data={"username": "email_0", "password": "password_1"}
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect username or password"
