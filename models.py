from database import Base
from sqlalchemy.orm import Mapped, mapped_column

class Expense(Base):
    __tablename__ = "expenses" # tell pyhton -> Expense Python class represents the expenses database table.

    id: Mapped[int] = mapped_column(primary_key=True) # id is a SQLAlchemy-mapped attribute whose Python type is int. and mapped_column(...) defines how that attribute becomes a database column.
    name: Mapped[str]
    amount: Mapped[float]
    category: Mapped[str]
    date: Mapped[str]
    payment: Mapped[str]