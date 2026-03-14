from database.db import db
from models.budget import Budget

class BudgetService:
    @staticmethod
    def add_budget(user_id, category, limit, month, year):
        budget = Budget(user_id=user_id, category=category, limit=limit, month=month, year=year)
        db.session.add(budget)
        db.session.commit()
        return budget
    
    @staticmethod
    def get_all_budgets(user_id):
        return Budget.query.filter_by(user_id=user_id).all()