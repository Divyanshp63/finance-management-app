from services.expense_service import ExpenseService
from services.saving_service import SavingService
from datetime import datetime, timedelta
from collections import defaultdict
import statistics

class PredictionService:
    """Predict future expenses and savings based on historical data"""
    
    @staticmethod
    def get_expense_forecast(user_id, months_back=3):
        """Predict next month's expenses based on past data"""
        expenses = ExpenseService.get_all_expenses(user_id)
        now = datetime.utcnow()
        
        # Collect data for past N months
        monthly_totals = defaultdict(float)
        monthly_by_category = defaultdict(lambda: defaultdict(list))
        
        for expense in expenses:
            months_ago = (now.year - expense.date.year) * 12 + (now.month - expense.date.month)
            if 0 <= months_ago <= months_back:
                month_key = f"{expense.date.year}-{expense.date.month:02d}"
                monthly_totals[month_key] += expense.amount
                monthly_by_category[expense.category][month_key].append(expense.amount)
        
        if not monthly_totals:
            return None
        
        # Calculate average monthly spending
        monthly_values = list(monthly_totals.values())
        if len(monthly_values) < 2:
            avg_monthly = monthly_values[0] if monthly_values else 0
        else:
            avg_monthly = statistics.mean(monthly_values)
        
        # Calculate variance to assess consistency
        if len(monthly_values) > 1:
            try:
                variance = statistics.stdev(monthly_values)
            except:
                variance = 0
        else:
            variance = 0
        
        confidence = "High" if variance < avg_monthly * 0.2 else "Medium" if variance < avg_monthly * 0.5 else "Low"
        
        return {
            'type': 'expense_forecast',
            'predicted_amount': avg_monthly,
            'variance': variance,
            'confidence': confidence,
            'message': f"Based on past {months_back} months, expect ₹{avg_monthly:.0f} spending next month ({confidence} confidence)",
            'emoji': '📊'
        }
    
    @staticmethod
    def get_category_forecast(user_id, months_back=3):
        """Predict spending by category for next month"""
        expenses = ExpenseService.get_all_expenses(user_id)
        now = datetime.utcnow()
        
        category_avg = defaultdict(list)
        
        for expense in expenses:
            months_ago = (now.year - expense.date.year) * 12 + (now.month - expense.date.month)
            if 0 <= months_ago <= months_back:
                category_avg[expense.category].append(expense.amount)
        
        forecast = {}
        for category, amounts in category_avg.items():
            avg = statistics.mean(amounts) if amounts else 0
            forecast[category] = {
                'predicted_amount': avg,
                'frequency': len(amounts)
            }
        
        return forecast
    
    @staticmethod
    def get_savings_forecast(user_id):
        """Predict next month's savings based on historical patterns"""
        savings = SavingService.get_all_savings(user_id)
        expenses = ExpenseService.get_all_expenses(user_id)
        
        now = datetime.utcnow()
        
        # Current month savings so far
        current_month_savings = [s for s in savings if 
                                  s.date.year == now.year and 
                                  s.date.month == now.month]
        current_saved = sum(s.amount for s in current_month_savings)
        
        # Current month expenses
        current_month_expenses = [e for e in expenses if 
                                   e.date.year == now.year and 
                                   e.date.month == now.month]
        current_spent = sum(e.amount for e in current_month_expenses)
        
        # Historical savings average
        all_month_savings = defaultdict(float)
        for saving in savings:
            month_key = f"{saving.date.year}-{saving.date.month:02d}"
            all_month_savings[month_key] += saving.amount
        
        if all_month_savings:
            avg_monthly_savings = statistics.mean(all_month_savings.values())
        else:
            avg_monthly_savings = 0
        
        return {
            'type': 'savings_forecast',
            'predicted_savings': avg_monthly_savings,
            'current_month_savings': current_saved,
            'message': f"You're on track to save ₹{avg_monthly_savings:.0f} next month",
            'emoji': '💚'
        }
    
    @staticmethod
    def get_spending_anomaly(user_id):
        """Detect if this week's spending is unusual"""
        expenses = ExpenseService.get_all_expenses(user_id)
        now = datetime.utcnow()
        
        # Current week (last 7 days)
        week_ago = now - timedelta(days=7)
        this_week = [e for e in expenses if e.date >= week_ago and e.date <= now]
        this_week_total = sum(e.amount for e in this_week)
        
        # Previous weeks
        previous_weeks = []
        for week_num in range(1, 5):  # Last 4 weeks
            week_start = now - timedelta(days=(7 * (week_num + 1)))
            week_end = now - timedelta(days=(7 * week_num))
            week_expenses = [e for e in expenses if e.date >= week_start and e.date <= week_end]
            week_total = sum(e.amount for e in week_expenses)
            if week_total > 0:
                previous_weeks.append(week_total)
        
        if not previous_weeks:
            return None
        
        avg_weekly = statistics.mean(previous_weeks)
        
        if avg_weekly == 0:
            return None
        
        change = ((this_week_total - avg_weekly) / avg_weekly) * 100
        
        if abs(change) > 30:
            return {
                'type': 'anomaly',
                'message': f"Your spending this week is {abs(change):.0f}% {'higher' if change > 0 else 'lower'} than usual",
                'emoji': '🚨' if change > 30 else '👍',
                'change_percentage': change,
                'this_week_amount': this_week_total,
                'average_weekly': avg_weekly
            }
        
        return None
    
    @staticmethod
    def get_all_predictions(user_id):
        """Get all predictions"""
        predictions = []
        
        forecast = PredictionService.get_expense_forecast(user_id)
        if forecast:
            predictions.append(forecast)
        
        savings_forecast = PredictionService.get_savings_forecast(user_id)
        if savings_forecast:
            predictions.append(savings_forecast)
        
        anomaly = PredictionService.get_spending_anomaly(user_id)
        if anomaly:
            predictions.append(anomaly)
        
        return predictions
