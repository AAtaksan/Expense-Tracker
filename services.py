import crud

class ExpenseLimitError(Exception):
    pass

class UserNotFoundError(Exception):
    pass

def create_expense(session, user_id, expense_data):

    user = crud.get_user_by_id(session, user_id)

    if user is None:
        raise UserNotFoundError(
            "User Not found"
        )
    # Business logic
    if expense_data.amount > 10000:
        raise ExpenseLimitError(
            "Expense amount cannot exceed ₹10,000"
        )

    # Database operation
    return crud.create_expense(session, user_id, expense_data)

def get_expenses(session, user_id):

    user = crud.get_user_by_id(session, user_id)

    if user is None:
        raise UserNotFoundError(
            "User Not found"
        )

    return crud.get_expenses(session, user_id)

def get_expense_by_id(session, user_id, expense_id):

    user = crud.get_user_by_id(session, user_id)

    if user is None:
        raise UserNotFoundError(
            "User Not Found"
        )

    return crud.get_expense_by_id(session, user_id, expense_id)

def update_expense(session, user_id, expense_id, expense_data):
    user = crud.get_user_by_id(session, user_id)

    if user is None:
        raise UserNotFoundError(
            "User Not Found"
        )

    if expense_data.amount > 10000:
        raise ExpenseLimitError(
            "Expense amount cannot exceed ₹10,000"
        )

    return crud.update_expense(session, user_id, expense_id, expense_data)

def delete_expense(session, user_id, expense_id):
    user = crud.get_user_by_id(session, user_id)

    if user is None:
        raise UserNotFoundError(
            "User Not Found"
        )

    return crud.delete_expense(session, user_id, expense_id)
