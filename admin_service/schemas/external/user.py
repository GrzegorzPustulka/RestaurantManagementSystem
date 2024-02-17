from uuid import UUID

from pydantic import BaseModel, EmailStr

from admin_service.models_choices import Role


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role: Role
    name: str
    surname: str
    phone: str
    street: str
    house_number: int
    flat_number: int | None = None
    city: str
    postal_code: str
    country: str


class UserUpdate(BaseModel):
    pass


class UserRead(BaseModel):
    id: UUID
    email: EmailStr
    role: Role


class UserDetailsRead(BaseModel):
    id: UUID
    user_id: UUID
    address_id: UUID
    name: str
    surname: str
    phone: str


class AddressRead(BaseModel):
    id: UUID
    street: str
    house_number: int
    flat_number: int | None = None
    city: str
    postal_code: str
    country: str


class EmployeeRead(BaseModel):
    user: UserRead
    user_details: UserDetailsRead
    user_address: AddressRead
