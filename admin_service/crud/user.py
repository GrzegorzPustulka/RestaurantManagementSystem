import bcrypt
from sqlalchemy import select, insert
from sqlalchemy.orm import Session

from admin_service.core.security import get_password_hash
from admin_service.models import Address, Users, UsersDetails
from admin_service.schemas.external.user import UserCreate, UserUpdate

from .base import CRUDBase


class CRUDUser(CRUDBase[Users, UserCreate, UserUpdate]):
    @staticmethod
    def get_by_email(db: Session, email: str) -> Users | None:
        return db.execute(
            select(Users).where(Users.email == email)
        ).scalar_one_or_none()

    def create(self, db: Session, obj_in: UserCreate) -> [Users, UsersDetails, Address]:
        hashed_password = get_password_hash(obj_in.password)
        user = Users(
            email=obj_in.email,
            password=hashed_password,
            role=obj_in.role,
        )
        db.execute(insert(Users).values(**user.as_dict()))
        db.commit()

        address = Address(
            street=obj_in.street,
            house_number=obj_in.house_number,
            flat_number=obj_in.flat_number,
            city=obj_in.city,
            postal_code=obj_in.postal_code,
            country=obj_in.country,
        )
        db.execute(insert(Address).values(**user.as_dict()))
        db.commit()

        user_details = UsersDetails(
            user_id=user.id,
            address_id=address.id,
            name=obj_in.name,
            surname=obj_in.surname,
            phone=obj_in.phone,
        )
        db.execute(insert(UsersDetails).values(**user.as_dict()))
        db.commit()

        return user, user_details, address


user = CRUDUser(Users)
