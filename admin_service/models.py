import uuid
from datetime import datetime
from uuid import UUID

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    declared_attr,
    mapped_column,
    relationship,
)


class Base(DeclarativeBase):
    id: Mapped[UUID] = mapped_column(
        primary_key=True, index=True, unique=True, default=uuid.uuid4
    )

    @declared_attr
    def __tablename__(cls) -> str:
        name = cls.__name__
        return "".join(["_" + c.lower() if c.isupper() else c for c in name]).lstrip(
            "_"
        )

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Users(Base):
    email: Mapped[str] = mapped_column(String(100))
    password: Mapped[str]
    role: Mapped[str]

    orders: Mapped["Orders"] = relationship(back_populates="users")
    details: Mapped["UsersDetails"] = relationship(back_populates="users")

    def __repr__(self):
        return f"Users(id={self.id!r}, email={self.email!r}, role={self.role!r})"


class UsersDetails(Base):
    name: Mapped[str] = mapped_column(String(50))
    surname: Mapped[str] = mapped_column(String(50))
    phone: Mapped[str | None] = mapped_column(String(15))

    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"))
    address_id: Mapped[UUID] = mapped_column(ForeignKey("address.id"))

    users: Mapped["Users"] = relationship(back_populates="details")
    address: Mapped["Address"] = relationship(back_populates="users")

    def __repr__(self):
        return f"UsersDetails(id={self.id!r}, user_id={self.user_id!r}, address_id={self.address_id!r}, name={self.name!r}, surname={self.surname!r}, phone={self.phone!r})"


class Address(Base):
    street: Mapped[str] = mapped_column(String(100))
    house_number: Mapped[int] = mapped_column(Integer)
    flat_number: Mapped[int | None] = mapped_column(Integer)
    city: Mapped[str] = mapped_column(String(100))
    postal_code: Mapped[str] = mapped_column(String(6))
    country: Mapped[str] = mapped_column(String(100))

    users: Mapped["UsersDetails"] = relationship(back_populates="address")
    suppliers: Mapped["Suppliers"] = relationship(back_populates="address")

    def __repr__(self):
        return f"Address(id={self.id!r}, street={self.street!r}, house_number={self.house_number!r}, flat_number={self.flat_number!r}, city={self.city!r}, postal_code={self.postal_code!r}, country={self.country!r})"


class Menu(Base):
    name: Mapped[str]
    description: Mapped[str | None]
    price: Mapped[float]
    category_id: Mapped[UUID] = mapped_column(ForeignKey("category.id"))

    order_details: Mapped["OrderDetails"] = relationship(back_populates="menu")
    category: Mapped["Category"] = relationship(back_populates="menu")

    def __repr__(self):
        return f"Menu(id={self.id!r}, name={self.name!r}, description={self.description!r}, price={self.price!r}, category_id={self.category_id!r})"


class Category(Base):
    name: Mapped[str]
    menu: Mapped["Menu"] = relationship(back_populates="category")

    def __repr__(self):
        return f"Category(id={self.id!r}, name={self.name!r})"


class Orders(Base):
    date: Mapped[datetime]
    status: Mapped[str]
    cost: Mapped[float]
    customer_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"))

    users: Mapped["Users"] = relationship(back_populates="orders")
    order_details: Mapped["OrderDetails"] = relationship(back_populates="order")

    def __repr__(self):
        return f"Orders(id={self.id!r}, customer_id={self.customer_id!r}, date={self.date!r}, status={self.status!r}, cost={self.cost!r})"


class OrderDetails(Base):
    quantity: Mapped[int]
    order_id: Mapped[UUID] = mapped_column(ForeignKey("orders.id"))
    menu_id: Mapped[UUID] = mapped_column(ForeignKey("menu.id"))

    order: Mapped["Orders"] = relationship(back_populates="order_details")
    menu: Mapped["Menu"] = relationship(back_populates="order_details")

    def __repr__(self):
        return f"OrderDetails(id={self.id!r}, order_id={self.order_id!r}, menu_id={self.menu_id!r}, quantity={self.quantity!r})"


class Inventory(Base):
    name: Mapped[str]
    quantity: Mapped[int]
    supplier_id: Mapped[UUID] = mapped_column(ForeignKey("suppliers.id"))

    supplier: Mapped["Suppliers"] = relationship(back_populates="inventory")

    def __repr__(self):
        return f"Inventory(id={self.id!r}, name={self.name!r}, quantity={self.quantity!r}, supplier_id={self.supplier_id!r})"


class Suppliers(Base):
    company: Mapped[str]
    contact: Mapped[str]
    address_id: Mapped[UUID] = mapped_column(ForeignKey("address.id"))

    address: Mapped["Address"] = relationship(back_populates="suppliers")
    inventory: Mapped["Inventory"] = relationship(back_populates="supplier")

    def __repr__(self):
        return f"Suppliers(id={self.id!r}, company={self.company!r}, contact={self.contact!r}, address_id={self.address_id!r})"
