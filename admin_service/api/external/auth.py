from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from admin_service.api.deps import get_db
from admin_service.core.auth import authenticate, create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/")
def login(
    db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    user = authenticate(email=form_data.username, password=form_data.password, db=db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    return {
        "access_token": create_access_token(sub=user.id),
        "token_type": "bearer",
    }
