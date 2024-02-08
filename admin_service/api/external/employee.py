from fastapi import APIRouter, Depends, HTTPException, status

from admin_service.api.deps import get_db
from admin_service.crud.employee import employee as crud_employee
from admin_service.schemas.external.employee import (
    AddressRead,
    EmployeeCreate,
    EmployeeRead,
    UserDetailsRead,
    UserRead,
)

router = APIRouter(prefix="/employee", tags=["employee"])


@router.post("/", status_code=status.HTTP_202_ACCEPTED, response_model=EmployeeRead)
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

    # todo: Send email to the user to confirm the account

    return employee_read
