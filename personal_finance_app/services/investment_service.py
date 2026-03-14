from database.db import db
from models.investment import Investment

class InvestmentService:
    @staticmethod
    def add_investment(user_id, type, amount):
        inv = Investment(user_id=user_id, type=type, amount=amount)
        db.session.add(inv)
        db.session.commit()
        return inv

    @staticmethod
    def get_all_investments(user_id):
        return Investment.query.filter_by(user_id=user_id).all()
    
    @staticmethod
    def delete_investment(investment_id, user_id):
        inv = Investment.query.filter_by(id=investment_id, user_id=user_id).first()
        if inv:
            db.session.delete(inv)
            db.session.commit()
            return True
        return False