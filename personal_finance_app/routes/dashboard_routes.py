from flask import Blueprint, render_template
from flask_login import login_required, current_user
from services.expense_service import ExpenseService
from services.budget_service import BudgetService
from services.saving_service import SavingService
from services.investment_service import InvestmentService
from services.insights_service import InsightsService
from services.alerts_service import AlertsService
from services.goal_service import GoalService

dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/")

@dashboard_bp.route("/")
@login_required
def dashboard():
    expenses = ExpenseService.get_all_expenses(current_user.id)
    budgets = BudgetService.get_all_budgets(current_user.id)
    savings = SavingService.get_all_savings(current_user.id)
    investments = InvestmentService.get_all_investments(current_user.id)
    
    total_expense = sum(e.amount for e in expenses) if expenses else 0
    total_budget = sum(b.limit for b in budgets) if budgets else 0
    total_saving = sum(s.amount for s in savings) if savings else 0
    total_investment = sum(i.amount for i in investments) if investments else 0
    
    # Get insights and alerts
    insights = InsightsService.get_all_insights(current_user.id)[:3]  # Show top 3
    alerts = AlertsService.get_all_alerts(current_user.id)[:3]  # Show top 3
    goals = GoalService.get_all_goals_progress(current_user.id)[:3]  # Show top 3
    
    return render_template(
        "index.html",
        expenses=expenses,
        total_expense=total_expense,
        total_budget=total_budget,
        total_saving=total_saving,
        total_investment=total_investment,
        insights=insights,
        alerts=alerts,
        goals=goals
    )

@dashboard_bp.route("/reports")
@login_required
def reports():
    expenses = ExpenseService.get_all_expenses(current_user.id)
    budgets = BudgetService.get_all_budgets(current_user.id)
    savings = SavingService.get_all_savings(current_user.id)
    investments = InvestmentService.get_all_investments(current_user.id)
    
    total_expense = sum(e.amount for e in expenses) if expenses else 0
    total_budget = sum(b.limit for b in budgets) if budgets else 0
    total_saving = sum(s.amount for s in savings) if savings else 0
    total_investment = sum(i.amount for i in investments) if investments else 0
    
    return render_template(
        "reports.html",
        total_expense=total_expense,
        total_budget=total_budget,
        total_saving=total_saving,
        total_investment=total_investment,
        expenses=expenses,
        budgets=budgets,
        savings=savings,
        investments=investments
    )