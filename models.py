from database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    email: Mapped[str]

    expenses: Mapped[list["Expense"]] = relationship(
        back_populates="user"
    )

class Expense(Base):
    __tablename__ = "expenses" # tell pyhton -> Expense Python class represents the expenses database table.

    id: Mapped[int] = mapped_column(primary_key=True) # id is a SQLAlchemy-mapped attribute whose Python type is int. and mapped_column(...) defines how that attribute becomes a database column.
    name: Mapped[str]
    amount: Mapped[float]
    category: Mapped[str]
    date: Mapped[str]
    payment: Mapped[str]

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id")
    )

    user: Mapped["User"] = relationship(
        back_populates="expenses"
    )