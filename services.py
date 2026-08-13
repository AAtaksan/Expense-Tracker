import crud

class ExpenseLimitError(Exception):
    pass

def create_expense(session, expense_data):

    # Business logic
    if expense_data.amount > 10000:
        raise ExpenseLimitError(
            "Expense amount cannot exceed ₹10,000"
        )

    # Database operation
    return crud.create_expense(session, expense_data)

def update_expense(session, expense_id, expense_data):

    if expense_data.amount > 10000:
        raise ExpenseLimitError(
            "Expense amount cannot exceed ₹10,000"
        )

    updated_expense = crud.update_expense(session, expense_id, expense_data)

    return updated_expense

def delete_expense(session, expense_id):
    deleted_expense = crud.delete_expense(session, expense_id)

    return deleted_expense