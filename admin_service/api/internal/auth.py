from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status

from admin_service.api.deps import get_db
from admin_service.crud.user import user as crud_admin
from admin_service.schemas.internal.admin import AdminCreate
from admin_service.utils.rabbitmq import RabbitMQPublisher

router = APIRouter(prefix="/internal", tags=["internal"])


@router.post("/signup", status_code=status.HTTP_204_NO_CONTENT, response_model=None)
async def create_admin(admin_in: AdminCreate, db=Depends(get_db)):
    if crud_admin.get_by_email(db, admin_in.email):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="The user.py with this email already exists in the system",
        )
    crud_admin.create(db=db, obj_in=admin_in)

    producer = RabbitMQPublisher()
    producer.publish(admin_in.email, admin_in.first_email)
    producer.close()
