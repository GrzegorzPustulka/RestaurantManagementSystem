from pydantic import SecretStr
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pytest
from admin_service.models import Base
from admin_service.core.config import Settings
from admin_service.api.deps import get_db
from admin_service.main import app
from fastapi.testclient import TestClient
from .fixtures import setup_db
from admin_service.core.auth import create_access_token, authenticate

settings = Settings(
    POSTGRES_USER="postgres",
    PGPASSWORD=SecretStr("secretPassword"),
    PGHOST="localhost",
    PGPORT=5432,
    PGDATABASE="postgres",
)

engine = create_engine(settings.sqlalchemy_database_uri)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def db():
    Base.metadata.create_all(bind=engine)
    with TestingSessionLocal() as db_session:
        setup_db(db_session)
        yield db_session
    Base.metadata.drop_all(bind=engine)


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture()
def client():
    with TestClient(app) as client:
        yield client


@pytest.fixture()
def token(db):
    user = authenticate(email="email_admin", password="password_admin", db=db)
    create_access_token(sub=user.id)
    return create_access_token(sub=user.id)


@pytest.fixture()
def auth_client(client, token):
    client.headers["Authorization"] = f"Bearer {token}"
    return client
