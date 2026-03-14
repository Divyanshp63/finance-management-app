from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from services.expense_service import ExpenseService

expense_bp = Blueprint("expense", __name__, url_prefix="/expense")

@expense_bp.route("/", methods=["GET", "POST"])
@login_required
def expense():
    if request.method == "POST":
        category = request.form["category"]
        amount = float(request.form["amount"])
        ExpenseService.add_expense(current_user.id, category, amount)
        return redirect(url_for("expense.expense"))
    expenses = ExpenseService.get_all_expenses(current_user.id)
    return render_template("expense.html", expenses=expenses)