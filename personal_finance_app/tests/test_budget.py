from app import app, db, Budget

def test_add_budget(client):
    with app.app_context():
        budget = Budget(category="Food", limit=5000)
        db.session.add(budget)
        db.session.commit()
        assert budget.id is not None
        assert budget.category == "Food"