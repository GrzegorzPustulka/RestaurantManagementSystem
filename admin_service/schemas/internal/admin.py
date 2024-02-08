from pydantic import BaseModel, EmailStr
from typing import Literal
from admin_service.models_choices import Role


class AdminCreate(BaseModel):
    email: EmailStr
    password: str
    role: Literal["ADMIN"] = "ADMIN"
    name: str
    surname: str
    phone: str
    street: str
    house_number: int
    flat_number: int | None = None
    city: str
    postal_code: str
    country: str
