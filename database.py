from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session

DATABASE_URL = "sqlite:///./expenses.db"

engine = create_engine(DATABASE_URL) # engine is the main entry point for SQLAlchemy to communicate with the database.

class Base(DeclarativeBase): # Classes that inherit from this base are going to describe database tables
    pass

def get_session():
    with Session(engine) as session:
        yield session

# Mock Session

# expense1 = Expense(
#     name = "Lunch",
#     amount = 250,
#     category = "Food",
#     date = "06-08-2026",
#     payment = "Cash",
# )


# with Session(engine, expire_on_commit=False) as session:
#     session.add(expense1) # Insert row
#     session.commit() # commit row
#     session.refresh(expense1)

#     statement = select(Expense) # read
#     result = session.execute(statement)
#     expenses = result.scalars().all()

#     statement2 = select(Expense).where(Expense.id == 2)
#     result2 = session.execute(statement2)
#     expense2 = result2.scalar_one()
#     expense2.amount = 300
#     session.commit()
#     session.refresh(expense2)

#     statement3 = select(Expense).where(Expense.id == 5)
#     result3 = session.execute(statement3)
#     expense3 = result3.scalar_one()
#     session.delete(expense3)
#     session.commit()

#     statement4 = select(Expense)
#     result4 = session.execute(statement4)
#     remaining_expenses = result4.scalars().all()


# for expense in remaining_expenses:
#     print(f"ID: {expense.id}")
#     print(f"Name: {expense.name}")
#     print(f"Amount: {expense.amount}")
#     print(f"Category: {expense.category}")