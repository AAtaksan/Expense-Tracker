from pydantic import BaseModel, Field, ConfigDict # Import Pydantic Model, Field
from enum import Enum

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
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    amount: float
    category: str
    date: str
    payment: str

class UserCreate(BaseModel):
    name: str = Field(min_length=1)
    email: str = Field(min_length=1)

class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int 
    name: str
    email: str