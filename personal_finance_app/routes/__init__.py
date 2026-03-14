from flask import Blueprint
from .auth_routes import auth_bp
from .advisor_routes import advisor_bp
from .budget_routes import budget_bp
from .expense_routes import expense_bp
from .investment_routes import investment_bp
from .saving_routes import saving_bp
from .dashboard_routes import dashboard_bp
from .goal_routes import goal_bp
from .insights_routes import insights_bp

def register_routes(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(advisor_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(budget_bp)
    app.register_blueprint(expense_bp)
    app.register_blueprint(investment_bp)
    app.register_blueprint(saving_bp)
    app.register_blueprint(goal_bp)
    app.register_blueprint(insights_bp)