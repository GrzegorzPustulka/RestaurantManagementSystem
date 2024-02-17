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


class EmailSubject(Enum):
    first_email = "First email"
    password_reset = "Password reset"
