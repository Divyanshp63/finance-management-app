from flask import Flask
from config import Config
from database.db import db
from flask_migrate import Migrate
from flask_login import LoginManager
from routes import register_routes
from models import Budget, Expense, Investment, Saving, User, Goal


app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "auth.login"
login_manager.login_message = "Please log in to access this page."

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ensure tables exist when the app starts (useful for development/demo)
# in production you might prefer running migrations explicitly via flask-migrate
with app.app_context():
    db.create_all()

register_routes(app)


if __name__ == "__main__":
    app.run(debug=True)