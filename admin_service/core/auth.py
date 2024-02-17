from datetime import UTC, datetime, timedelta
from typing import MutableMapping

from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from sqlalchemy.orm import Session

from admin_service.core.config import settings
from admin_service.core.security import verify_password
from admin_service.models import Users

JWTPayloadMapping = MutableMapping[str, datetime | bool | str | list[str] | list[int]]

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def authenticate(email: str, password: str, db: Session) -> Users | None:
    user = db.query(Users).filter(Users.email == email).first()
    if not user:
        return None
    if not verify_password(password, user.password):
        return None
    return user


def create_access_token(sub: str) -> str:
    return _create_access_token(
        token_type="access_token",
        lifetime=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        sub=sub,
    )


def _create_access_token(token_type: str, lifetime: timedelta, sub: str) -> str:
    payload = {}
    expire = datetime.now(UTC) + lifetime
    payload["type"] = token_type
    payload["exp"] = expire
    payload["iat"] = datetime.now(UTC)
    payload["sub"] = str(sub)

    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.ALGORITHM)
