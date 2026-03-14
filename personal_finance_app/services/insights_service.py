from services.expense_service import ExpenseService
from services.budget_service import BudgetService
from datetime import datetime, timedelta
from collections import defaultdict

class InsightsService:
    """Generate smart insights about spending patterns"""
    
    @staticmethod
    def get_overspending_alerts(user_id):
        """Check which categories are overspending"""
        alerts = []
        budgets = BudgetService.get_all_budgets(user_id)
        expenses = ExpenseService.get_all_expenses(user_id)
        
        # Group expenses by category
        expenses_by_category = defaultdict(float)
        for expense in expenses:
            expenses_by_category[expense.category] += expense.amount
        
        # Check against budgets
        for budget in budgets:
            spent = expenses_by_category.get(budget.category, 0)
            if spent > budget.limit:
                overage = spent - budget.limit
                percentage = (overage / budget.limit) * 100
                alerts.append({
                    'type': 'overspending',
                    'category': budget.category,
                    'message': f"You are overspending in {budget.category} by ₹{overage:.2f} ({percentage:.0f}% over)",
                    'emoji': '⚠',
                    'severity': 'high' if percentage > 25 else 'medium',
                    'amount': overage
                })
        
        return alerts
    
    @staticmethod
    def get_spending_trend(user_id):
        """Compare current month spending with previous month"""
        expenses = ExpenseService.get_all_expenses(user_id)
        now = datetime.utcnow()
        
        # Current month expenses
        current_month_expenses = [e for e in expenses if 
                                   e.date.year == now.year and 
                                   e.date.month == now.month]
        current_total = sum(e.amount for e in current_month_expenses)
        
        # Previous month expenses
        prev_month = now - timedelta(days=30)
        prev_month_expenses = [e for e in expenses if 
                               e.date.year == prev_month.year and 
                               e.date.month == prev_month.month]
        prev_total = sum(e.amount for e in prev_month_expenses)
        
        if prev_total == 0:
            return None
        
        change = ((current_total - prev_total) / prev_total) * 100
        
        if abs(change) < 5:
            message = f"Your spending is stable at ₹{current_total:.2f} 📊"
        elif change < -10:
            message = f"Great! Your spending decreased by {abs(change):.0f}% 👏"
            emoji = '📉'
        elif change > 10:
            message = f"Your spending increased by {change:.0f}% - be careful! 📈"
            emoji = '⚠'
        else:
            message = f"Your spending changed by {change:+.0f}% 📈"
            emoji = '📊'
        
        return {
            'type': 'trend',
            'message': message,
            'emoji': emoji,
            'change_percentage': change,
            'current_amount': current_total,
            'previous_amount': prev_total
        }
    
    @staticmethod
    def get_savings_insight(user_id):
        """Calculate savings rate and provide insight"""
        expenses = ExpenseService.get_all_expenses(user_id)
        budgets = BudgetService.get_all_budgets(user_id)
        
        now = datetime.utcnow()
        current_month_expenses = [e for e in expenses if 
                                   e.date.year == now.year and 
                                   e.date.month == now.month]
        
        total_budget = sum(b.limit for b in budgets 
                          if b.year == now.year and b.month == now.month)
        total_expense = sum(e.amount for e in current_month_expenses)
        
        if total_budget == 0:
            return None
        
        savings = total_budget - total_expense
        savings_rate = (savings / total_budget) * 100
        
        if savings > 0:
            message = f"You can save ₹{savings:.0f} more by reducing discretionary expenses 💰"
            emoji = '💚'
        else:
            message = f"You're overspending by ₹{abs(savings):.0f} - reduce unnecessary expenses! ⚠"
            emoji = '❌'
        
        return {
            'type': 'savings',
            'message': message,
            'emoji': emoji,
            'savings_amount': savings,
            'savings_rate': savings_rate
        }
    
    @staticmethod
    def get_category_comparison(user_id):
        """Find which category takes most of your money"""
        expenses = ExpenseService.get_all_expenses(user_id)
        
        now = datetime.utcnow()
        current_month_expenses = [e for e in expenses if 
                                   e.date.year == now.year and 
                                   e.date.month == now.month]
        
        if not current_month_expenses:
            return None
        
        # Group by category
        by_category = defaultdict(float)
        for expense in current_month_expenses:
            by_category[expense.category] += expense.amount
        
        if not by_category:
            return None
        
        top_category = max(by_category.items(), key=lambda x: x[1])
        total = sum(by_category.values())
        percentage = (top_category[1] / total) * 100
        
        return {
            'type': 'category',
            'message': f"{top_category[0]} is your biggest expense at ₹{top_category[1]:.0f} ({percentage:.0f}% of total)",
            'emoji': '🎯',
            'category': top_category[0],
            'amount': top_category[1],
            'percentage': percentage
        }
    
    @staticmethod
    def get_all_insights(user_id):
        """Get all available insights"""
        insights = []
        
        overspending = InsightsService.get_overspending_alerts(user_id)
        if overspending:
            insights.extend(overspending)
        
        trend = InsightsService.get_spending_trend(user_id)
        if trend:
            insights.append(trend)
        
        savings = InsightsService.get_savings_insight(user_id)
        if savings:
            insights.append(savings)
        
        category = InsightsService.get_category_comparison(user_id)
        if category:
            insights.append(category)
        
        return insights
