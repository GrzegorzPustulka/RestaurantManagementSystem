from typing import Annotated, Generator

from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from pydantic import BaseModel
from sqlalchemy.orm import Session

from admin_service.core.auth import oauth2_scheme
from admin_service.core.config import settings
from admin_service.database import SessionLocal
from admin_service.models import Users


class TokenData(BaseModel):
    username: str | None = None


def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
) -> Users:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.ALGORITHM],
            options={"verify_aud": False},
        )
        username: str = payload.get("sub")
        if not username:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception

    user = db.query(Users).filter(Users.id == token_data.username).first()
    if user is None:
        raise credentials_exception

    return user


User = Annotated[Users, Depends(get_current_user)]
DB = Annotated[Session, Depends(get_db)]
Token = Annotated[str, Depends(oauth2_scheme)]
