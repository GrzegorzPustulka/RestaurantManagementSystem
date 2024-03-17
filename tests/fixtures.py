import random
from uuid import UUID

from admin_service.models_choices import Role
from tests.factories import (
    CreateObjectCommand,
    UserFactory,
    UserDetailFactory,
    AddressFactory,
    Factory,
    MenuFactory,
    CategoryFactory,
)
from admin_service.core.security import get_password_hash
from sqlalchemy.orm import Session

categories_id = []
menu_id = []


def setup_db(db: Session):
    users = [
        CreateObjectCommand(
            db,
            UserFactory,
            email=f"email_{i}",
            password=get_password_hash(f"password_{i}"),
            role=random.choice(list(Role)).value,
        ).execute()
        for i in range(5)
    ]
    users_id = [user.id for user in users]

    CreateObjectCommand(
        db,
        UserFactory,
        email=f"email_admin",
        password=get_password_hash("password_admin"),
        role=Role.ADMIN.value,
    ).execute()

    addresses = [
        CreateObjectCommand(
            db,
            AddressFactory,
            street=f"street_{i}",
            house_number=f"{i}",
            flat_number=f"{i}" if i % 2 == 0 else None,
            city=f"city_{i}",
            postal_code=f"{i}",
            country=f"Poland{i}",
        ).execute()
        for i in range(5)
    ]
    addresses_id = [address.id for address in addresses]

    _ = [
        CreateObjectCommand(
            db,
            UserDetailFactory,
            name=f"Name_{i}",
            surname=f"Surname_{i}",
            phone=f"123456789",
            user_id=users_id[i],
            address_id=addresses_id[i],
        ).execute()
        for i in range(5)
    ]

    categories = [
        CreateObjectCommand(
            db,
            CategoryFactory,
            name=f"Category_{i}",
        ).execute()
        for i in range(5)
    ]
    categories_id.clear()
    categories_id.extend([str(category.id) for category in categories])

    menu = [
        CreateObjectCommand(
            db,
            MenuFactory,
            name=f"Menu_{i}",
            description=f"Description_{i}",
            price=10.0,
            category_id=UUID(categories_id[i]),
        ).execute()
        for i in range(5)
    ]
    menu_id.clear()
    menu_id.extend([str(m.id) for m in menu])
