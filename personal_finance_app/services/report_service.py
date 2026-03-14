from app import db, Expense, Saving, Investment

class ReportService:
    @staticmethod
    def get_summary():
        total_expenses = sum([e.amount for e in Expense.query.all()])
        total_savings = sum([s.amount for s in Saving.query.all()])
        total_investments = sum([i.amount for i in Investment.query.all()])

        return {
            "total_expenses": total_expenses,
            "total_savings": total_savings,
            "total_investments": total_investments
        }