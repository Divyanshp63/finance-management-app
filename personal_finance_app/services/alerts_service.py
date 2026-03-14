from services.expense_service import ExpenseService
from services.budget_service import BudgetService
from services.saving_service import SavingService
from datetime import datetime, timedelta
from collections import defaultdict

class AlertsService:
    """Generate smart alerts based on spending patterns and budgets"""
    
    @staticmethod
    def get_budget_alerts(user_id):
        """Check for budget exceeded alerts"""
        alerts = []
        budgets = BudgetService.get_all_budgets(user_id)
        expenses = ExpenseService.get_all_expenses(user_id)
        
        now = datetime.utcnow()
        
        # Group expenses by category and current month
        expenses_by_category = defaultdict(float)
        for expense in expenses:
            if expense.date.year == now.year and expense.date.month == now.month:
                expenses_by_category[expense.category] += expense.amount
        
        for budget in budgets:
            if budget.year == now.year and budget.month == now.month:
                spent = expenses_by_category.get(budget.category, 0)
                percentage = (spent / budget.limit * 100) if budget.limit > 0 else 0
                
                if percentage >= 100:
                    overage = spent - budget.limit
                    alerts.append({
                        'type': 'budget_exceeded',
                        'category': budget.category,
                        'message': f"🚨 Budget Exceeded! {budget.category} is over by ₹{overage:.0f}",
                        'severity': 'critical',
                        'percentage': percentage,
                        'spent': spent,
                        'limit': budget.limit
                    })
                elif percentage >= 80:
                    remaining = budget.limit - spent
                    alerts.append({
                        'type': 'budget_warning',
                        'category': budget.category,
                        'message': f"⚠ High Spending Alert! You've used {percentage:.0f}% of {budget.category} budget. Only ₹{remaining:.0f} left",
                        'severity': 'warning',
                        'percentage': percentage,
                        'spent': spent,
                        'limit': budget.limit
                    })
        
        return alerts
    
    @staticmethod
    def get_low_savings_alerts(user_id):
        """Alert if savings are below expected"""
        alerts = []
        savings = SavingService.get_all_savings(user_id)
        
        now = datetime.utcnow()
        
        # Check current month savings
        current_month_savings = [s for s in savings if 
                                 s.date.year == now.year and 
                                 s.date.month == now.month]
        current_saved = sum(s.amount for s in current_month_savings)
        
        # Check expected savings (assume 20% of income)
        # For now, use a fixed threshold
        expected_minimum = 5000  # ₹5000 minimum savings expected
        
        if current_saved < expected_minimum:
            alerts.append({
                'type': 'low_savings',
                'message': f"💰 Low Savings Alert! You've saved only ₹{current_saved:.0f} this month. Target: ₹{expected_minimum}",
                'severity': 'warning',
                'current': current_saved,
                'target': expected_minimum
            })
        
        return alerts
    
    @staticmethod
    def get_unusual_expense_alerts(user_id):
        """Alert for unusual expenses compared to normal patterns"""
        alerts = []
        expenses = ExpenseService.get_all_expenses(user_id)
        
        now = datetime.utcnow()
        today = datetime.combine(now.date(), datetime.min.time())
        
        # Get today's expenses
        today_expenses = [e for e in expenses if 
                         datetime.combine(e.date.date(), datetime.min.time()) == today]
        
        today_total = sum(e.amount for e in today_expenses)
        
        # Get average daily spending for this month
        month_expenses = [e for e in expenses if 
                         e.date.year == now.year and 
                         e.date.month == now.month]
        
        if month_expenses:
            days_in_month = len(set(e.date.date() for e in month_expenses))
            if days_in_month > 0:
                avg_daily = sum(e.amount for e in month_expenses) / days_in_month
                
                if today_total > avg_daily * 1.5:  # 50% more than average
                    excess = today_total - (avg_daily * 1.5)
                    alerts.append({
                        'type': 'unusual_expense',
                        'message': f"⚡ Unusual Spending! Today's spending (₹{today_total:.0f}) is 50% higher than your daily average",
                        'severity': 'info',
                        'today_amount': today_total,
                        'average_daily': avg_daily,
                        'excess': excess
                    })
        
        return alerts
    
    @staticmethod
    def get_category_spike_alerts(user_id):
        """Alert for unusual spike in specific category"""
        alerts = []
        expenses = ExpenseService.get_all_expenses(user_id)
        
        now = datetime.utcnow()
        
        # Get last 7 days expenses by category
        week_ago = now - timedelta(days=7)
        week_expenses = defaultdict(list)
        
        for expense in expenses:
            if week_ago <= expense.date <= now:
                week_expenses[expense.category].append(expense.amount)
        
        # Get previous month average for each category
        prev_month_start = datetime(now.year, now.month - 1, 1) if now.month > 1 else datetime(now.year - 1, 12, 1)
        prev_month_expenses = defaultdict(list)
        
        for expense in expenses:
            if expense.date >= prev_month_start and expense.date < datetime(now.year, now.month, 1):
                prev_month_expenses[expense.category].append(expense.amount)
        
        # Check for spikes
        for category, amounts in week_expenses.items():
            if len(amounts) > 0:
                week_total = sum(amounts)
                prev_avg = sum(prev_month_expenses.get(category, [])) / len(prev_month_expenses.get(category, [1])) if prev_month_expenses.get(category) else 0
                
                if prev_avg > 0 and week_total > prev_avg * 1.5:
                    change_percent = ((week_total - prev_avg) / prev_avg) * 100
                    alerts.append({
                        'type': 'category_spike',
                        'category': category,
                        'message': f"📈 {category} spending spiked {change_percent:.0f}% higher than last month!",
                        'severity': 'warning',
                        'current_week': week_total,
                        'previous_avg': prev_avg,
                        'spike_percentage': change_percent
                    })
        
        return alerts
    
    @staticmethod
    def get_all_alerts(user_id):
        """Get all alerts consolidated"""
        all_alerts = []
        
        # Budget alerts
        budget_alerts = AlertsService.get_budget_alerts(user_id)
        if budget_alerts:
            all_alerts.extend(budget_alerts)
        
        # Low savings alerts
        savings_alerts = AlertsService.get_low_savings_alerts(user_id)
        if savings_alerts:
            all_alerts.extend(savings_alerts)
        
        # Unusual expense alerts
        unusual_alerts = AlertsService.get_unusual_expense_alerts(user_id)
        if unusual_alerts:
            all_alerts.extend(unusual_alerts)
        
        # Category spike alerts
        spike_alerts = AlertsService.get_category_spike_alerts(user_id)
        if spike_alerts:
            all_alerts.extend(spike_alerts)
        
        # Sort by severity
        severity_order = {'critical': 0, 'warning': 1, 'info': 2}
        all_alerts.sort(key=lambda x: severity_order.get(x.get('severity', 'info'), 2))
        
        return all_alerts
