from sqlalchemy import select
from sqlalchemy.orm import Session

from models import Expense

def create_expense(session: Session, expense_data):
    new_expense = Expense(
        name=expense_data.name,
        amount=expense_data.amount,
        category=expense_data.category,
        date=expense_data.date,
        payment=expense_data.payment
    )
    
    try:
        session.add(new_expense)
        session.commit()
    except Exception:
        session.rollback()
        raise

    session.refresh(new_expense)

    return new_expense

def get_expenses(session: Session):
    statement = select(Expense)
    result = session.execute(statement)
    expenses = result.scalars().all()
    return expenses

def get_expense_by_id(session: Session, expense_id: int):
    statement = select(Expense).where(Expense.id == expense_id)
    result = session.execute(statement)
    expense = result.scalar_one_or_none()
    return expense

def update_expense(session: Session, expense_id: int, expense_data):
    stored_expense = get_expense_by_id(session, expense_id)
    
    if stored_expense is None:
        return None

    stored_expense.name = expense_data.name
    stored_expense.amount = expense_data.amount
    stored_expense.category = expense_data.category
    stored_expense.date = expense_data.date
    stored_expense.payment = expense_data.payment

    try:
        session.commit()
    except Exception:
        session.rollback()
        raise
    session.refresh(stored_expense)

    return stored_expense

def delete_expense(session: Session, expense_id: int):
    expense = get_expense_by_id(session, expense_id)
    
    if expense is None:
        return None

    try:
        session.delete(expense)
        session.commit()
    except Exception:
        session.rollback()
        raise
    return expense