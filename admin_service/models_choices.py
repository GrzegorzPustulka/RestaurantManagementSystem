from enum import Enum


class Role(Enum):
    ADMIN = "admin"
    COOK = "cook"
    waiter = "waiter"
    CLIENT = "client"


class Status(Enum):
    NEW = "new"
    IN_PROGRESS = "in_progress"
    READY = "ready"
    DELIVERED = "delivered"
