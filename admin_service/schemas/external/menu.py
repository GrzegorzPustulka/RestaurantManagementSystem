from uuid import UUID

from pydantic import BaseModel, field_validator


class MenuBase(BaseModel):
    name: str
    description: str | None = None
    price: float


class MenuCreate(MenuBase):
    category_id: UUID

    @field_validator("name")
    @classmethod
    def make_capitalize(cls, v: str) -> str:
        return v.capitalize()

    @field_validator("description")
    @classmethod
    def make_sentence(cls, v: str) -> str:
        if v:
            return (v.capitalize()).rstrip(".") + "."


class MenuUpdate(MenuCreate):
    category_id: UUID | None = None

    def model_dump(self, **kwargs) -> dict:
        return {k: v for k, v in dict(self).items() if v is not None}


class MenuRead(MenuBase):
    id: UUID
    category_id: UUID
