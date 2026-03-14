from database.db import db
from models.expense import Expense

class ExpenseService:
    @staticmethod
    def add_expense(user_id, category, amount):
        expense = Expense(user_id=user_id, category=category, amount=amount)
        db.session.add(expense)
        db.session.commit()
        return expense

    @staticmethod
    def get_all_expenses(user_id):
        return Expense.query.filter_by(user_id=user_id).all()