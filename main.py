from fastapi import FastAPI, HTTPException, Depends # Import FastAPI class, HTTPException for HTTP errors
from sqlalchemy.orm import Session
from database import Base, engine, get_session
from schemas import (
    ExpenseCreate,
    ExpenseResponse,
    UserCreate,
    UserResponse
)
import crud
import services

Base.metadata.create_all(engine)

app = FastAPI() # Creates your FastAPI application object

@app.get("/") # create an endpoit that tell when a client send a GET request to this path then execute the function below
def home(): # Endpoint function which handles the request
    return {"message": "AI Expense Tracker API"} # FastAPI automatically converts the Python dictionary into a JSON response.

# User API 
@app.post("/users", response_model=UserResponse, status_code=201)
def create_user(user: UserCreate, session: Session = Depends(get_session)):
    return crud.create_user(session, user)

@app.get("/users", response_model=list[UserResponse])
def get_users(session: Session = Depends(get_session)):
    return crud.get_users(session)

@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int, session: Session = Depends(get_session)):
    user = crud.get_user_by_id(session, user_id)

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User Not Found"
        )

    return user

@app.post("/users/{user_id}/expenses", response_model=ExpenseResponse, status_code=201) # create a Post method to create expenses
def create_expense(user_id: int, expense: ExpenseCreate, session: Session = Depends(get_session)):
    try:
        return services.create_expense(session, user_id, expense)
    except services.UserNotFoundError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error)
        )
    except services.ExpenseLimitError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

@app.get("/users/{user_id}/expenses", response_model=list[ExpenseResponse]) # a response model defines the structure, fields, and types of the response
def display_expenses(user_id: int, session: Session = Depends(get_session)):
    try: 
        return services.get_expenses(session, user_id)
    except services.UserNotFoundError as error:
        raise HTTPException(
            status_code=404, 
            detail=str(error)
        )

@app.get("/users/{user_id}/expenses/{expense_id}", response_model=ExpenseResponse) # path parameter: FastAPI pulls expense_id from the URL
def get_expense(user_id: int, expense_id: int, session: Session = Depends(get_session)):
    try:
        expense = services.get_expense_by_id(session, user_id, expense_id)
    except services.UserNotFoundError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error)
        )

    if expense is None:
        raise HTTPException(
            status_code=404,
            detail="Expense not found"
        )

    return expense

@app.put("/users/{user_id}/expenses/{expense_id}", response_model=ExpenseResponse)
def update_expense(user_id: int, expense_id: int, expense: ExpenseCreate, session: Session = Depends(get_session)): # expense_id -> path parameter and expense: ExpenseCreate -> Request Body
    try:
        updated_expense = services.update_expense(session, user_id, expense_id, expense)

    except services.UserNotFoundError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error)
        )

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

@app.delete("/users/{user_id}/expenses/{expense_id}", response_model=ExpenseResponse)
def delete_expense(user_id: int, expense_id: int, session: Session = Depends(get_session)):
    try:
        deleted_expense = services.delete_expense(session, user_id, expense_id)
    except services.UserNotFoundError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error)
        )

    if deleted_expense is None:
        raise HTTPException(
            status_code=404,
            detail="Expense Not Found"
        )

    return deleted_expense
