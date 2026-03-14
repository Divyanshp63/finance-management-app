from app import app, db, Saving

def test_add_saving(client):
    with app.app_context():
        saving = Saving(goal="Emergency Fund", amount=15000)
        db.session.add(saving)
        db.session.commit()
        assert saving.id is not None
        assert saving.goal == "Emergency Fund"