from fastapi import APIRouter, Depends, HTTPException, status
from admin_service.crud.employee import employee as crud_employee
from admin_service.schemas.employee import (
    EmployeeCreate,
    EmployeeRead,
    EmployeeUpdate,
    UserRead,
    UserDetailsRead,
    AddressRead,
)
from admin_service.api.deps import get_db
from admin_service.utils.smtp_integration import SMTPManager

router = APIRouter(prefix="/employee", tags=["employee"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=EmployeeRead)
async def create_employee(employee_in: EmployeeCreate, db=Depends(get_db)):
    if crud_employee.get_by_email(db, employee_in.email):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="The user with this email already exists in the system",
        )

    user, user_details, user_address = crud_employee.create(db=db, obj_in=employee_in)
    employee_read = EmployeeRead(
        user=UserRead(**user.as_dict()),
        user_details=UserDetailsRead(**user_details.as_dict()),
        user_address=AddressRead(**user_address.as_dict()),
    )

    # Send email to the user
    stmp_manager: SMTPManager = SMTPManager(user.email)
    stmp_manager.send_email(subject="DineStream - first login", file_name="first_login")

    return employee_read
