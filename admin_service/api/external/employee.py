from fastapi import APIRouter, Depends, HTTPException, status

from admin_service.api.deps import DB, User, get_db
from admin_service.crud.user import user as crud_employee
from admin_service.models_choices import EmailSubject
from admin_service.schemas.external.user import (
    AddressRead,
    EmployeeRead,
    UserCreate,
    UserDetailsRead,
    UserRead,
)
from admin_service.utils.rabbitmq import RabbitMQPublisher

router = APIRouter(prefix="/employee", tags=["employee"])


@router.post("/", status_code=status.HTTP_202_ACCEPTED, response_model=EmployeeRead)
async def create_employee(employee_in: UserCreate, db: DB, _: User):
    if crud_employee.get_by_email(db, employee_in.email):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="The user.py with this email already exists in the system",
        )

    user, user_details, user_address = crud_employee.create(db=db, obj_in=employee_in)
    employee_read = EmployeeRead(
        user=UserRead(**user.as_dict()),
        user_details=UserDetailsRead(**user_details.as_dict()),
        user_address=AddressRead(**user_address.as_dict()),
    )

    producer = RabbitMQPublisher()
    producer.publish(employee_in.email, EmailSubject.first_email)
    producer.close()

    return employee_read
