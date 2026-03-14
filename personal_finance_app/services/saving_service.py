from database.db import db
from models.saving import Saving

class SavingService:
    @staticmethod
    def add_saving(user_id, goal, amount):
        saving = Saving(user_id=user_id, goal=goal, amount=amount)
        db.session.add(saving)
        db.session.commit()
        return saving

    @staticmethod
    def get_all_savings(user_id):
        return Saving.query.filter_by(user_id=user_id).all()