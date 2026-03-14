from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from services.budget_service import BudgetService

budget_bp = Blueprint("budget", __name__, url_prefix="/budget")

@budget_bp.route("/", methods=["GET", "POST"])
@login_required
def budget():
    if request.method == "POST":
        category = request.form["category"]
        limit = float(request.form["limit"])
        month = int(request.form["month"])
        year = int(request.form["year"])
        BudgetService.add_budget(current_user.id, category, limit, month, year)
        return redirect(url_for("budget.budget"))
    budgets = BudgetService.get_all_budgets(current_user.id)
    return render_template("budget.html", budgets=budgets)