import bcrypt
from sqlalchemy.orm import Session

from admin_service.models import Address, Users, UsersDetails
from admin_service.schemas.employee import EmployeeCreate

from .base import CRUDBase


class CRUDMenu(CRUDBase[Users, EmployeeCreate, EmployeeCreate]):
    @staticmethod
    def get_by_email(db: Session, email: str) -> Users | None:
        return db.query(Users).filter(Users.email == email).one_or_none()

    def create(
        self, db: Session, obj_in: EmployeeCreate
    ) -> [Users, UsersDetails, Address]:
        hashed_password = bcrypt.hashpw(
            obj_in.password.encode("utf-8"), bcrypt.gensalt()
        )
        user = Users(
            email=obj_in.email,
            password=hashed_password,
            role=obj_in.role,
        )
        db.add(user)
        db.commit()

        address = Address(
            street=obj_in.street,
            house_number=obj_in.house_number,
            flat_number=obj_in.flat_number,
            city=obj_in.city,
            postal_code=obj_in.postal_code,
            country=obj_in.country,
        )
        db.add(address)
        db.commit()

        user_details = UsersDetails(
            user_id=user.id,
            address_id=address.id,
            name=obj_in.name,
            surname=obj_in.surname,
            phone=obj_in.phone,
        )
        db.add(user_details)
        db.commit()

        return user, user_details, address


employee = CRUDMenu(Users)
