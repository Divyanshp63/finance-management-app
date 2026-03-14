from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from services.investment_advisor import InvestmentAdvisor

advisor_bp = Blueprint("advisor", __name__, url_prefix="/advisor")


@advisor_bp.route("/", methods=["GET"])
@login_required
def advisor():
    """Display investment advisor recommendations"""
    advisor_data = InvestmentAdvisor.get_recommendations(current_user.id)
    
    return render_template(
        "advisor.html",
        summary=advisor_data['summary'],
        recommendations=advisor_data['recommendations']
    )


@advisor_bp.route("/summary", methods=["GET"])
@login_required
def summary():
    """Display financial summary"""
    summary = InvestmentAdvisor.get_user_summary(current_user.id)
    
    return render_template("advisor_summary.html", summary=summary)
