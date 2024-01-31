from sqlalchemy.orm import Session

from admin_service.models import Menu
from admin_service.schemas.menu import MenuCreate, MenuUpdate

from .base import CRUDBase


class CRUDMenu(CRUDBase[Menu, MenuCreate, MenuUpdate]):
    pass


menu = CRUDMenu(Menu)
