from fastapi import FastAPI, HTTPException, Depends # Import FastAPI class, HTTPException for HTTP errors
from sqlalchemy.orm import Session
from database import Base, engine, get_session
from schemas import ExpenseCreate, ExpenseResponse
import crud
import services

Base.metadata.create_all(engine)

app = FastAPI() # Creates your FastAPI application object

@app.get("/") # create an endpoit that tell when a client send a GET request to this path then execute the function below
def home(): # Endpoint function which handles the request
    return {"message": "AI Expense Tracker API"} # FastAPI automatically converts the Python dictionary into a JSON response.

@app.post("/expenses", response_model=ExpenseResponse, status_code=201) # create a Post method to create expenses
def create_expense(expense: ExpenseCreate, session: Session = Depends(get_session)):
    try:
        return services.create_expense(session, expense)
    except services.ExpenseLimitError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

@app.get("/expenses", response_model=list[ExpenseResponse]) # a response model defines the structure, fields, and types of the response
def display_expenses(session: Session = Depends(get_session)):
    return crud.get_expenses(session)

@app.get("/expenses/{expense_id}", response_model=ExpenseResponse) # path parameter: FastAPI pulls expense_id from the URL
def get_expense(expense_id: int, session: Session = Depends(get_session)):
    expense = crud.get_expense_by_id(session, expense_id)

    if expense is None:
        raise HTTPException(
            status_code=404,
            detail="Expense not found"
        )

    return expense

@app.put("/expenses/{expense_id}", response_model=ExpenseResponse)
def update_expense(expense_id: int, expense: ExpenseCreate, session: Session = Depends(get_session)): # expense_id -> path parameter and expense: ExpenseCreate -> Request Body
    try:
        updated_expense = services.update_expense(session, expense_id, expense)

    except services.ExpenseLimitError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    if updated_expense is None:
        raise HTTPException(
            status_code=404,
            detail="Expense Not Found"
        )
    
    return updated_expense

@app.delete("/expenses/{expense_id}", response_model=ExpenseResponse)
def delete_expense(expense_id: int, session: Session = Depends(get_session)):
    deleted_expense = services.delete_expense(session, expense_id)

    if deleted_expense is None:
        raise HTTPException(
            status_code=404,
            detail="Expense Not Found"
        )

    return deleted_expense
