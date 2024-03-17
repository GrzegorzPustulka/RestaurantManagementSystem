from typing import Generic, Type, TypeVar

from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import select, update, delete, insert

from admin_service.models import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    def get(self, db: Session, id: str) -> ModelType | None:
        return db.execute(
            select(self.model).where(self.model.id == id)
        ).scalar_one_or_none()

    def get_all(self, db: Session) -> list[ModelType]:
        return db.scalars(select(self.model)).all()  # type: ignore

    def create(self, db: Session, obj_in: CreateSchemaType) -> ModelType:
        result = db.execute(
            insert(self.model).values(obj_in.model_dump()).returning(self.model)
        )
        db.commit()
        return result.scalar_one()

    def update(self, db: Session, id: str, obj_in: UpdateSchemaType) -> ModelType:
        result = db.execute(
            update(self.model)
            .where(self.model.id == id)
            .values(obj_in.model_dump())
            .returning(self.model)
        )
        db.commit()
        return result.scalar_one()

    def remove(self, db: Session, id: str) -> ModelType:
        result = db.execute(
            delete(self.model).where(self.model.id == id).returning(self.model)
        )
        db.commit()
        return result.scalar_one()
