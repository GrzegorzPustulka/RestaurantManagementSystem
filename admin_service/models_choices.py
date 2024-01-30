from enum import Enum


class Role(Enum):
    ADMIN = 'admin'
    COOK = 'cook'
    waiter = 'waiter'


class Category(Enum):
    MAIN_COURSE = 'main_course'
    SOUP = 'soup'
    DESSERT = 'dessert'
    DRINK = 'drink'


class Status(Enum):
    NEW = 'new'
    IN_PROGRESS = 'in_progress'
    READY = 'ready'
    DELIVERED = 'delivered'
