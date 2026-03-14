from models.goal import Goal
from database.db import db

class GoalService:
    """Service for managing financial goals"""
    
    @staticmethod
    def add_goal(user_id, name, emoji, target_amount, current_amount, deadline_months):
        """Create a new goal"""
        goal = Goal(
            user_id=user_id,
            name=name,
            emoji=emoji,
            target_amount=target_amount,
            current_amount=current_amount,
            deadline_months=deadline_months
        )
        db.session.add(goal)
        db.session.commit()
        return goal
    
    @staticmethod
    def get_all_goals(user_id):
        """Get all goals for a user"""
        return Goal.query.filter_by(user_id=user_id).all()
    
    @staticmethod
    def get_goal_by_id(goal_id, user_id):
        """Get a goal by ID"""
        return Goal.query.filter_by(id=goal_id, user_id=user_id).first()
    
    @staticmethod
    def update_goal(goal_id, user_id, name=None, emoji=None, target_amount=None, 
                    current_amount=None, deadline_months=None):
        """Update a goal"""
        goal = Goal.query.filter_by(id=goal_id, user_id=user_id).first()
        if goal:
            if name is not None:
                goal.name = name
            if emoji is not None:
                goal.emoji = emoji
            if target_amount is not None:
                goal.target_amount = target_amount
            if current_amount is not None:
                goal.current_amount = current_amount
            if deadline_months is not None:
                goal.deadline_months = deadline_months
            
            db.session.commit()
        return goal
    
    @staticmethod
    def add_to_goal(goal_id, user_id, amount):
        """Add money to a goal"""
        goal = Goal.query.filter_by(id=goal_id, user_id=user_id).first()
        if goal:
            goal.current_amount += amount
            db.session.commit()
        return goal
    
    @staticmethod
    def delete_goal(goal_id, user_id):
        """Delete a goal"""
        goal = Goal.query.filter_by(id=goal_id, user_id=user_id).first()
        if goal:
            db.session.delete(goal)
            db.session.commit()
        return True
    
    @staticmethod
    def get_goal_progress(goal_id, user_id):
        """Get progress info for a goal"""
        goal = Goal.query.filter_by(id=goal_id, user_id=user_id).first()
        if not goal:
            return None
        
        progress_percentage = goal.get_progress_percentage()
        monthly_target = goal.get_monthly_target()
        
        return {
            'goal': goal,
            'progress_percentage': progress_percentage,
            'remaining_amount': max(0, goal.target_amount - goal.current_amount),
            'monthly_target': monthly_target,
            'is_complete': progress_percentage >= 100,
            'message': f"Save ₹{monthly_target:.0f}/month for {goal.deadline_months} months to reach ₹{goal.target_amount:.0f}"
        }
    
    @staticmethod
    def get_all_goals_progress(user_id):
        """Get progress for all goals for a user"""
        goals = Goal.query.filter_by(user_id=user_id).all()
        progress_list = []
        
        for goal in goals:
            progress_list.append(GoalService.get_goal_progress(goal.id, user_id))
        
        return progress_list
