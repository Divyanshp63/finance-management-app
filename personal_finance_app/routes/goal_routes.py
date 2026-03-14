from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from flask_login import login_required, current_user
from services.goal_service import GoalService

goal_bp = Blueprint("goal", __name__, url_prefix="/goal")

@goal_bp.route("/", methods=["GET", "POST"])
@login_required
def goals():
    if request.method == "POST":
        name = request.form.get("name")
        emoji = request.form.get("emoji", "🎯")
        target_amount = float(request.form.get("target_amount", 0))
        deadline_months = int(request.form.get("deadline_months", 6))
        
        GoalService.add_goal(current_user.id, name, emoji, target_amount, 0, deadline_months)
        return redirect(url_for("goal.goals"))
    
    goals = GoalService.get_all_goals(current_user.id)
    goals_progress = GoalService.get_all_goals_progress(current_user.id)
    
    return render_template("goals.html", goals=goals, goals_progress=goals_progress)

@goal_bp.route("/<int:goal_id>/update", methods=["POST"])
@login_required
def update_goal(goal_id):
    current_amount = float(request.form.get("current_amount", 0))
    GoalService.update_goal(goal_id, current_user.id, current_amount=current_amount)
    return redirect(url_for("goal.goals"))

@goal_bp.route("/<int:goal_id>/add", methods=["POST"])
@login_required
def add_to_goal(goal_id):
    amount = float(request.form.get("amount", 0))
    GoalService.add_to_goal(goal_id, current_user.id, amount)
    return redirect(url_for("goal.goals"))

@goal_bp.route("/<int:goal_id>/delete", methods=["POST"])
@login_required
def delete_goal(goal_id):
    GoalService.delete_goal(goal_id, current_user.id)
    return redirect(url_for("goal.goals"))

@goal_bp.route("/<int:goal_id>/progress")
@login_required
def goal_progress(goal_id):
    progress = GoalService.get_goal_progress(goal_id, current_user.id)
    if progress:
        return jsonify(progress)
    return jsonify({'error': 'Goal not found'}), 404
