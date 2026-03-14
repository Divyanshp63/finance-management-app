import pytest
import importlib.util
import os

# load the blueprint-based application from finance-app.py (hyphen not importable normally)
spec = importlib.util.spec_from_file_location("finance_app", os.path.join(os.path.dirname(__file__), "..", "finance-app.py"))
finance_app = importlib.util.module_from_spec(spec)
spec.loader.exec_module(finance_app)

app = finance_app.app
from database.db import db

@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()