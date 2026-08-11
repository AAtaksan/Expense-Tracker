from fastapi import FastAPI, HTTPException # Import FastAPI class, HTTPException for HTTP errors
from pydantic import BaseModel, Field # Import Pydantic Model, Field
from enum import Enum

app = FastAPI() # Creates your FastAPI application object

@app.get("/") # create an endpoit that tell when a client send a GET request to this path then execute the function below
def home(): # Endpoint function which handles the request
    return {"message": "AI Expense Tracker API"} # FastAPI automatically converts the Python dictionary into a JSON response.

expenses = []
next_id = 1 # separate counter, independent of len(expenses), so deletions never cause a collision
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

@app.post("/expenses", response_model=ExpenseResponse, status_code=201) # create a Post method to create expenses
def create_expense(expense: ExpenseCreate):
    global next_id # tell Python we're modifying the module-level next_id, not creating a local one
    expense_dict = expense.model_dump() # Covert Python Object into Dictionary using model_dump()
    expense_dict["id"] = next_id #len(expenses) + 1 # Generate the next id from the current length of the list
    expenses.append(expense_dict) 
    next_id += 1
    return expense_dict

@app.get("/expenses", response_model=list[ExpenseResponse]) # a response model defines the structure, fields, and types of the response
def display_expenses():
    return expenses

@app.get("/expenses/{expense_id}", response_model=ExpenseResponse) # path parameter: FastAPI pulls expense_id from the URL
def get_expense(expense_id: int):
    for expense in expenses:
        if expense["id"] == expense_id:
            return expense 

    raise HTTPException(
        status_code=404,
        detail="Expense not found"
    )

@app.put("/expenses/{expense_id}", response_model=ExpenseResponse)
def update_expense(expense_id: int, expense: ExpenseCreate): # expense_id -> path parameter and expense: ExpenseCreate -> Request Body
    for index, stored_expense in enumerate(expenses):
        if stored_expense["id"] == expense_id:
            updated_expense = expense.model_dump() # Convert the incoming request body into a dict
            updated_expense["id"] = expense_id # Preserve the original id, since ExpenseCreate has no id field
            expenses[index] = updated_expense # Replace the old dict at this position with the new one
            return updated_expense
 
    raise HTTPException(
        status_code=404,
        detail="Expense not found"
    )

@app.delete("/expenses/{expense_id}", response_model=ExpenseResponse)
def delete_expense(expense_id: int):
    for index, stored_expense in enumerate(expenses):
        if stored_expense["id"] == expense_id:
            deleted_expense = expenses.pop(index) # pop(index) remove expense from list and return it. 
            return deleted_expense

    raise HTTPException(
        status_code=404,
        detail="Expense Not Found"
    )
