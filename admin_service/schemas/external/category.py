from uuid import UUID

from pydantic import BaseModel, field_validator


class CategoryBase(BaseModel):
    name: str

    @field_validator("name")
    @classmethod
    def make_capitalize(cls, v: str) -> str:
        return v.capitalize()


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(CategoryBase):
    pass


class CategoryRead(CategoryBase):
    id: UUID
