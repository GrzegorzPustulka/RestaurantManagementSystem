from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from admin_service.api.deps import get_current_user, get_db
from admin_service.crud.category import category as crud_category
from admin_service.models import Users
from admin_service.schemas.external.category import (
    CategoryCreate,
    CategoryRead,
    CategoryUpdate,
)

router = APIRouter(prefix="/category", tags=["category"])
User = Annotated[Users, Depends(get_current_user)]
DB = Annotated[Session, Depends(get_db)]


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=CategoryRead)
async def create_category(category_in: CategoryCreate, db: DB, _: User):
    return crud_category.create(db=db, obj_in=category_in)


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[CategoryRead])
def read_category_all(db: DB, _: User):
    category = crud_category.get_all(db=db)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Category not found"
        )
    return category


@router.patch(
    "/{category_id}", status_code=status.HTTP_200_OK, response_model=CategoryRead
)
async def update_category(
    category_id: str, category_in: CategoryUpdate, db: DB, _: User
):
    category = crud_category.update(db=db, id=category_id, obj_in=category_in)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Category not found"
        )
    return category


@router.delete(
    "/{category_id}", status_code=status.HTTP_200_OK, response_model=CategoryRead
)
async def delete_category(category_id: str, db: DB, _: User):
    category = crud_category.remove(db=db, id=category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Category not found"
        )
    return category
