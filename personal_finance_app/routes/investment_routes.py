from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from services.investment_service import InvestmentService

investment_bp = Blueprint("investment", __name__, url_prefix="/investment")

@investment_bp.route("/", methods=["GET", "POST"])
@login_required
def investment():
    if request.method == "POST":
        type = request.form["type"]
        amount = float(request.form["amount"])
        InvestmentService.add_investment(current_user.id, type, amount)
        return redirect(url_for("investment.investment"))
    investments = InvestmentService.get_all_investments(current_user.id)
    return render_template("investments.html", investments=investments)