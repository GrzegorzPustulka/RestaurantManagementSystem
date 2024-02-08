from admin_service.models import Menu
from admin_service.schemas.external.menu import MenuCreate, MenuUpdate

from .base import CRUDBase


class CRUDMenu(CRUDBase[Menu, MenuCreate, MenuUpdate]):
    pass


menu = CRUDMenu(Menu)
