from uuid import UUID

from pydantic import BaseModel, field_validator


class MenuBase(BaseModel):
    name: str
    description: str | None
    price: float
    category_id: UUID


class MenuCreate(MenuBase):
    @field_validator("name")
    @classmethod
    def make_capitalize(cls, v: str) -> str:
        return v.capitalize()

    @field_validator("description")
    @classmethod
    def make_sentence(cls, v: str) -> str:
        if v:
            return (v.capitalize()).rstrip(".") + "."


class MenuUpdate(MenuBase):
    pass


class MenuRead(MenuBase):
    id: UUID
