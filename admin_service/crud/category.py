from admin_service.models import Category
from admin_service.schemas.category import CategoryCreate, CategoryUpdate

from .base import CRUDBase


class CRUDCategory(CRUDBase[Category, CategoryCreate, CategoryUpdate]):
    pass


category = CRUDCategory(Category)
