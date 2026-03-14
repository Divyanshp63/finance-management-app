from app import app, db, Expense


def test_add_expense(client):
    with app.app_context():
        expense = Expense(category="Travel", amount=1200)
        db.session.add(expense)
        db.session.commit()
        assert expense.id is not None
        assert expense.amount == 1200