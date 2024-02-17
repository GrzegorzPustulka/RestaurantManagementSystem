from pydantic import BaseModel, EmailStr

from admin_service.models_choices import Role


class AdminCreate(BaseModel):
    email: EmailStr
    password: str
    role: str = Role.ADMIN
    name: str
    surname: str
    phone: str
    street: str
    house_number: int
    flat_number: int | None = None
    city: str
    postal_code: str
    country: str
