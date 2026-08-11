from fastapi import FastAPI, HTTPException # Import FastAPI class, HTTPException for HTTP errors
from pydantic import BaseModel, Field # Import Pydantic Model, Field

app = FastAPI() # Creates your FastAPI application object

@app.get("/") # create an endpoit that tell when a client send a GET request to this path then execute the function below
def home(): # Endpoint function which handles the request
    return {"message": "AI Expense Tracker API"} # FastAPI automatically converts the Python dictionary into a JSON response.

expenses = []
class ExpenseCreate(BaseModel): # with pydantic model, FastAPI automatically converts the Python dictionary into a JSON response.
    name: str
    amount: float = Field(gt=0)
    category: str
    date: str
    payment: str

@app.post("/expenses") # create a Post method to create expenses
def create_expense(expense: ExpenseCreate):
    expense_dict = expense.model_dump() # Covert Python Object into Dictionary using model_dump()
    expense_dict["id"] = len(expenses) + 1 # Generate the next id from the current length of the list
    expenses.append(expense_dict) 
    return expense_dict

@app.get("/expenses")
def display_expenses():
    return expenses

@app.get("/expenses/{expense_id}") # path parameter: FastAPI pulls expense_id from the URL
def get_expense(expense_id: int):
    for expense in expenses:
        if expense["id"] == expense_id:
            return expense 

    raise HTTPException(
        status_code=404,
        detail="Expense not found"
    )

@app.put("/expenses/{expense_id}")
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

@app.delete("/expenses/{expense_id}")
def delete_expense(expense_id: int):
    for index, stored_expesne in enumerate(expenses):
        if stored_expesne["id"] == expense_id:
            delete_expense = expenses.pop(index)
            return delete_expense

    raise HTTPException(
        status_code=404,
        detail="Expense Not Found"
    )

