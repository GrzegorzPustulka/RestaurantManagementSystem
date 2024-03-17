from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from ..conftest import auth_client, db
from ..fixtures import categories_id, menu_id


def test_create_category(auth_client: TestClient, db: Session):
    response = auth_client.post(
        "/category/",
        json={"name": "name"},
    )
    assert response.status_code == 201
    assert response.json() == {
        "id": response.json()["id"],
        "name": "Name",
    }


def test_read_category_all(auth_client: TestClient, db: Session):
    response = auth_client.get("/category/")
    assert response.status_code == 200
    assert len(response.json()) == 5


def test_read_category(auth_client: TestClient, db: Session):
    response = auth_client.get(f"/category/{categories_id[0]}/")
    assert response.status_code == 200
    assert response.json() == {
        "id": categories_id[0],
        "name": "Category_0",
    }


def test_update_category(auth_client: TestClient, db: Session):
    response = auth_client.patch(
        f"/category/{categories_id[0]}/",
        json={"name": "new name"},
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": categories_id[0],
        "name": "New name",
    }


def test_delete_category_integrity_error(auth_client: TestClient, db: Session):
    response = auth_client.delete(f"/category/{categories_id[0]}/")
    assert response.status_code == 409
    assert response.json() == {
        "detail": "Cannot delete the record due to associated records in other tables."
    }


def test_delete_category(auth_client: TestClient, db: Session):
    response = auth_client.delete(f"/menu/{menu_id[0]}/")
    assert response.status_code == 200

    response = auth_client.delete(f"/category/{categories_id[0]}/")
    assert response.status_code == 200
    assert response.json() == {
        "id": categories_id[0],
        "name": "Category_0",
    }
