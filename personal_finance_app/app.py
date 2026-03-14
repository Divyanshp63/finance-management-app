from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from config import Config
from datetime import datetime

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)


class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Float, nullable=False)


@app.route("/")
def index():
    expenses = Expense.query.all()
    return render_template("index.html", expenses=expenses)


class Budget(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50), nullable=False)
    limit = db.Column(db.Float, nullable=False)


class Investment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)


class Saving(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    goal = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Float, nullable=False)


if __name__ == "__main__":
    app.run(debug=True)
