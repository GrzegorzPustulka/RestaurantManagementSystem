from abc import ABC, abstractmethod
from sqlalchemy.orm import Session
from uuid import UUID
from admin_service.models import (
    Users,
    UsersDetails,
    Address,
    Menu,
    Category,
    Orders,
    OrderDetails,
    Inventory,
    Suppliers,
)


class Command(ABC):
    @abstractmethod
    def execute(self):
        pass


class CreateObjectCommand(Command):
    def __init__(self, db: Session, factory, **kwargs):
        self.db = db
        self.factory = factory
        self.kwargs = kwargs

    def execute(self):
        obj = self.factory.create(**self.kwargs)
        self.db.add(obj)
        self.db.commit()
        return obj


class Factory(ABC):
    @staticmethod
    @abstractmethod
    def create(**kwargs):
        pass


class UserFactory(Factory):
    @staticmethod
    def create(
        email: str,
        password: str,
        role: str,
    ):
        return Users(
            email=email,
            password=password,
            role=role,
        )


class UserDetailFactory(Factory):
    @staticmethod
    def create(
        name: str,
        surname: str,
        phone: str | None,
        user_id: UUID,
        address_id: UUID,
    ):
        return UsersDetails(
            user_id=user_id,
            address_id=address_id,
            name=name,
            surname=surname,
            phone=phone,
        )


class AddressFactory(Factory):
    @staticmethod
    def create(
        street: str,
        house_number: int,
        flat_number: int | None,
        city: str,
        postal_code: str,
        country: str,
    ):
        return Address(
            street=street,
            house_number=house_number,
            flat_number=flat_number,
            city=city,
            postal_code=postal_code,
            country=country,
        )


class MenuFactory(Factory):
    @staticmethod
    def create(
        name: str,
        description: str | None,
        price: float,
        category_id: UUID,
    ):
        return Menu(
            name=name,
            description=description,
            price=price,
            category_id=category_id,
        )


class CategoryFactory(Factory):
    @staticmethod
    def create(
        name: str,
    ):
        return Category(
            name=name,
        )
