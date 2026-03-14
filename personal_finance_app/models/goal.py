from database.db import db
from datetime import datetime

class Goal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    emoji = db.Column(db.String(10), nullable=False, default="🎯")
    target_amount = db.Column(db.Float, nullable=False)
    current_amount = db.Column(db.Float, nullable=False, default=0)
    deadline_months = db.Column(db.Integer, nullable=False)  # months to reach goal
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"<Goal {self.name}: {self.current_amount}/{self.target_amount}>"

    def get_progress_percentage(self):
        if self.target_amount == 0:
            return 0
        return (self.current_amount / self.target_amount) * 100

    def get_monthly_target(self):
        """Calculate required monthly savings to reach goal"""
        if self.deadline_months <= 0:
            return self.target_amount
        remaining = self.target_amount - self.current_amount
        return remaining / self.deadline_months if remaining > 0 else 0
