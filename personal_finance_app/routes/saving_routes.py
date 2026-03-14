from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from services.saving_service import SavingService

saving_bp = Blueprint("saving", __name__, url_prefix="/saving")

@saving_bp.route("/", methods=["GET", "POST"])
@login_required
def saving():
    if request.method == "POST":
        goal = request.form["goal"]
        amount = float(request.form["amount"])
        SavingService.add_saving(current_user.id, goal, amount)
        return redirect(url_for("saving.saving"))
    savings = SavingService.get_all_savings(current_user.id)
    return render_template("saving.html", savings=savings)