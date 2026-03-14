from app import app, db, Investment

def test_add_investment(client):
    with app.app_context():
        inv = Investment(type="Stocks", amount=10000)
        db.session.add(inv)
        db.session.commit()
        assert inv.id is not None
        assert inv.type == "Stocks"