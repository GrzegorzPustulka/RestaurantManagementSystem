from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import DeclarativeBase, declared_attr, Mapped, mapped_column, relationship
from uuid import UUID
from datetime import datetime

from admin_service.models_choices import Category, Status, Role


class Base(DeclarativeBase):
    id: Mapped[UUID] = mapped_column(primary_key=True, index=True, unique=True)

    @declared_attr
    def __tablename__(cls) -> str:
        name = cls.__name__
        return ''.join(['_' + c.lower() if c.isupper() else c for c in name]).lstrip('_')


class Users(Base):
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    surname: Mapped[str] = mapped_column(String(50), nullable=False)
    phone: Mapped[str] = mapped_column(String(15), nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False)
    password: Mapped[str]
    address_id: Mapped[UUID] = mapped_column(ForeignKey('address.id'))

    address: Mapped["Address"] = relationship(back_populates="users")

    def __repr__(self):
        return f"User(id={self.id!r}, name={self.name!r}, surname={self.surname!r}, phone={self.phone!r}, email={self.email!r}, password={self.password!r}, address_id={self.address_id!r})"


class Address(Base):
    street: Mapped[str] = mapped_column(String(100))
    house_number: Mapped[int] = mapped_column(Integer)
    flat_number: Mapped[int | None] = mapped_column(Integer)
    city: Mapped[str] = mapped_column(String(100))
    postal_code: Mapped[str] = mapped_column(String(6))
    country: Mapped[str] = mapped_column(String(100))

    users: Mapped["Users"] = relationship("Users", back_populates="address")

    def __repr__(self):
        return f"Address(id={self.id!r}, street={self.street!r}, house_number={self.house_number!r}, flat_number={self.flat_number!r}, city={self.city!r}, postal_code={self.postal_code!r}, country={self.country!r})"


class Menu(Base):
    name: Mapped[str]
    description: Mapped[str | None]
    price: Mapped[float]
    category: Mapped[Category]

    order_details: Mapped["OrderDetails"] = relationship("OrderDetails", back_populates="menu")

    def __repr__(self):
        return f"Menu(id={self.id!r}, name={self.name!r}, description={self.description!r}, price={self.price!r}, category={self.category!r})"


class Orders(Base):
    date: Mapped[datetime]
    status: Mapped[Status]
    cost: Mapped[float]
    customer_id: Mapped[UUID] = mapped_column(ForeignKey('users.id'))

    customer: Mapped["Users"] = relationship("Users", back_populates="orders")
    order_details: Mapped["OrderDetails"] = relationship("OrderDetails", back_populates="order")

    def __repr__(self):
        return f"Orders(id={self.id!r}, customer_id={self.customer_id!r}, date={self.date!r}, status={self.status!r}, cost={self.cost!r})"


class OrderDetails(Base):
    quantity: Mapped[int]
    order_id: Mapped[UUID] = mapped_column(ForeignKey('orders.id'))
    menu_id: Mapped[UUID] = mapped_column(ForeignKey('menu.id'))

    order: Mapped["Orders"] = relationship("Orders", back_populates="order_details")
    menu: Mapped["Menu"] = relationship("Menu", back_populates="order_details")

    def __repr__(self):
        return f"OrderDetails(id={self.id!r}, order_id={self.order_id!r}, menu_id={self.menu_id!r}, quantity={self.quantity!r})"


class Inventory(Base):
    name: Mapped[str]
    quantity: Mapped[int]
    supplier_id: Mapped[UUID] = mapped_column(ForeignKey('suppliers.id'))

    supplier: Mapped["Suppliers"] = relationship("Suppliers", back_populates="inventory")

    def __repr__(self):
        return f"Inventory(id={self.id!r}, name={self.name!r}, quantity={self.quantity!r}, supplier_id={self.supplier_id!r})"


class Employees(Base):
    name: Mapped[str] = mapped_column(String(50))
    surname: Mapped[str] = mapped_column(String(50))
    phone: Mapped[str] = mapped_column(String(15))
    email: Mapped[str] = mapped_column(String(100))
    role: Mapped[Role]
    address_id: Mapped[UUID] = mapped_column(ForeignKey('address.id'))

    address: Mapped["Address"] = relationship("Address", back_populates="employees")

    def __repr__(self):
        return f"Employees(id={self.id!r}, name={self.name!r}, surname={self.surname!r}, phone={self.phone!r}, email={self.email!r}, role={self.role!r}, address_id={self.address_id!r})"


class Suppliers(Base):
    company: Mapped[str]
    contact: Mapped[str]
    address_id: Mapped[UUID] = mapped_column(ForeignKey('address.id'))

    address: Mapped["Address"] = relationship("Address", back_populates="suppliers")
    inventory: Mapped["Inventory"] = relationship("Inventory", back_populates="supplier")

    def __repr__(self):
        return f"Suppliers(id={self.id!r}, company={self.company!r}, contact={self.contact!r}, address_id={self.address_id!r})"