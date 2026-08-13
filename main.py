from fastapi import FastAPI, HTTPException, Depends # Import FastAPI class, HTTPException for HTTP errors
from pydantic import BaseModel, Field # Import Pydantic Model, Field
from enum import Enum
from database import Expense, get_session
from sqlalchemy import select
from sqlalchemy.orm import Session

app = FastAPI() # Creates your FastAPI application object

@app.get("/") # create an endpoit that tell when a client send a GET request to this path then execute the function below
def home(): # Endpoint function which handles the request
    return {"message": "AI Expense Tracker API"} # FastAPI automatically converts the Python dictionary into a JSON response.

class PaymentMethod(str, Enum):
    CASH = "Cash"
    UPI = "UPI"
    CARD = "Card"
class ExpenseCreate(BaseModel): # with pydantic model, FastAPI automatically converts the Python dictionary into a JSON response.
    name: str = Field(min_length=1)
    amount: float = Field(gt=0)
    category: str = Field(min_length=1)
    date: str = Field(min_length=1)
    payment: PaymentMethod

class ExpenseResponse(BaseModel):
    id: int
    name: str
    amount: float
    category: str
    date: str
    payment: str

def get_expense_by_id(session: Session, expense_id: int):
    statement = select(Expense).where(Expense.id == expense_id)
    result = session.execute(statement)
    expense = result.scalar_one_or_none()
    return expense

@app.post("/expenses", response_model=ExpenseResponse, status_code=201) # create a Post method to create expenses
def create_expense(expense: ExpenseCreate, session: Session = Depends(get_session)):
    new_expense = Expense(
        name=expense.name,
        amount=expense.amount,
        category=expense.category,
        date=expense.date,
        payment=expense.payment
    )

    try:
        session.add(new_expense)
        session.commit()
    except Exception:
        session.rollback()
        raise

    session.refresh(new_expense)

    return new_expense

@app.get("/expenses", response_model=list[ExpenseResponse]) # a response model defines the structure, fields, and types of the response
def display_expenses(session: Session = Depends(get_session)):
    statement = select(Expense)
    result = session.execute(statement)
    expenses = result.scalars().all()
    return expenses

@app.get("/expenses/{expense_id}", response_model=ExpenseResponse) # path parameter: FastAPI pulls expense_id from the URL
def get_expense(expense_id: int, session: Session = Depends(get_session)):
    expense = get_expense_by_id(session, expense_id)

    if expense is None:
        raise HTTPException(
            status_code=404,
            detail="Expense not found"
        )

    return expense

@app.put("/expenses/{expense_id}", response_model=ExpenseResponse)
def update_expense(expense_id: int, expense: ExpenseCreate, session: Session = Depends(get_session)): # expense_id -> path parameter and expense: ExpenseCreate -> Request Body
    stored_expense = get_expense_by_id(session, expense_id)

    if stored_expense is None:
        raise HTTPException(
            status_code=404,
            detail="Expense not found"
        )

    stored_expense.name = expense.name
    stored_expense.amount = expense.amount
    stored_expense.category = expense.category
    stored_expense.date = expense.date
    stored_expense.payment = expense.payment

    try:
        session.commit()
    except Exception:
        session.rollback()
        raise
    session.refresh(stored_expense)

    return stored_expense

@app.delete("/expenses/{expense_id}", response_model=ExpenseResponse)
def delete_expense(expense_id: int, session: Session = Depends(get_session)):
    expense = get_expense_by_id(session, expense_id)

    if expense is None:
        raise HTTPException(
            status_code=404,
            detail="Expense Not Found"
        )

    try:
        session.delete(expense)
        session.commit()
    except Exception:
        session.rollback()
        raise
    return expense
