from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from ..conftest import client, db, auth_client  # noqa (imported but unused)
from ..fixtures import categories_id, menu_id


def test_create_menu(db: Session, auth_client: TestClient):
    menu_data = {
        "name": "test menu",
        "description": "test description",
        "price": 10.0,
        "category_id": categories_id[0],
    }
    response = auth_client.post("/menu/", json=menu_data)
    assert response.status_code == 201
    assert response.json() == {
        "name": "Test menu",
        "description": "Test description.",
        "price": 10.0,
        "category_id": categories_id[0],
        "id": response.json()["id"],
    }


def test_read_all_menu(db: Session, auth_client: TestClient):
    response = auth_client.get("/menu/")
    assert response.status_code == 200
    assert len(response.json()) == 5


def test_read_menu(db: Session, auth_client: TestClient):
    response = auth_client.get(f"/menu/{menu_id[0]}")
    assert response.status_code == 200
    assert response.json() == {
        "name": "Menu_0",
        "description": "Description_0",
        "price": 10.0,
        "category_id": categories_id[0],
        "id": menu_id[0],
    }


def test_update_menu(db: Session, auth_client: TestClient):
    menu_data = {"name": "new name", "description": "new description", "price": 30.0}
    response = auth_client.patch(f"/menu/{menu_id[0]}", json=menu_data)
    assert response.status_code == 200
    assert response.json() == {
        "name": "New name",
        "description": "New description.",
        "price": 30.0,
        "category_id": categories_id[0],
        "id": menu_id[0],
    }


def test_delete_menu(db: Session, auth_client: TestClient):
    _ = auth_client.delete(f"/menu/{menu_id[0]}")
    response = auth_client.get(f"/menu/{menu_id[0]}")
    assert response.status_code == 404
    assert response.json() == {"detail": "Menu not found"}
