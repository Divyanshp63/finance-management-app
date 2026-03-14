from database.db import db
from models.saving import Saving
from models.expense import Expense
from models.investment import Investment
from datetime import datetime, timedelta
from sqlalchemy import func, extract


class InvestmentAdvisor:
    """Rule-based investment advisor system"""
    
    @staticmethod
    def get_user_summary(user_id):
        """Get financial summary for a user"""
        # Calculate total savings
        total_savings = db.session.query(func.sum(Saving.amount)).filter_by(user_id=user_id).scalar() or 0
        
        # Calculate monthly expenses (last 30 days)
        last_month = datetime.utcnow() - timedelta(days=30)
        monthly_expenses = db.session.query(func.sum(Expense.amount)).filter(
            Expense.user_id == user_id,
            Expense.date >= last_month
        ).scalar() or 0
        
        # Calculate total investments
        total_investments = db.session.query(func.sum(Investment.amount)).filter_by(user_id=user_id).scalar() or 0
        
        # Get investment breakdown by type
        investments_by_type = db.session.query(
            Investment.type,
            func.sum(Investment.amount).label('total')
        ).filter_by(user_id=user_id).group_by(Investment.type).all()
        
        investment_breakdown = {inv_type: total for inv_type, total in investments_by_type}
        
        return {
            'total_savings': total_savings,
            'monthly_expenses': monthly_expenses,
            'total_investments': total_investments,
            'investment_breakdown': investment_breakdown
        }
    
    @staticmethod
    def get_recommendations(user_id):
        """Generate investment recommendations based on rules"""
        summary = InvestmentAdvisor.get_user_summary(user_id)
        recommendations = []
        
        total_savings = summary['total_savings']
        monthly_expenses = summary['monthly_expenses']
        total_investments = summary['total_investments'] # Added this line to define total_investments
        
        # Rule 1: Check emergency fund status
        total_savings = total_savings or 0.0
        total_investments = total_investments or 0.0
        monthly_expenses = monthly_expenses or 0.0
        
        emergency_fund_needed = monthly_expenses * 3
        current_emergency_fund = total_savings
        
        emergency_fund_is_secure = current_emergency_fund >= emergency_fund_needed

        if not emergency_fund_is_secure:
            recommendations.append({
                'priority': 1,
                'title': '🚨 Build Emergency Fund (Top Priority)',
                'description': f'Your emergency fund should be ₹{emergency_fund_needed:.2f} (3 months of expenses). Currently, it is ₹{current_emergency_fund:.2f}.',
                'current': current_emergency_fund,
                'required': emergency_fund_needed,
                'action': f'Build up ₹{emergency_fund_needed - current_emergency_fund:.2f} more before investing elsewhere.',
                'reason': 'Emergency fund is your financial safety net. It must be completed before starting risky investments like stocks.',
                'progress_pct': (current_emergency_fund / emergency_fund_needed) * 100 if emergency_fund_needed > 0 else 0,
                'progress_style': f"{(current_emergency_fund / emergency_fund_needed) * 100 if emergency_fund_needed > 0 else 0:.1f}%"
            })
        else:
            recommendations.append({
                'priority': 4,
                'title': '✅ Emergency Fund Secure',
                'description': f'You have ₹{current_emergency_fund:.2f} saved (covers {current_emergency_fund/monthly_expenses if monthly_expenses > 0 else "all"} months).',
                'current': current_emergency_fund,
                'required': emergency_fund_needed,
                'action': 'Maintain this fund.',
                'reason': 'Your safety net is ready. You can now focus on wealth creation.',
                'progress_pct': 100,
                'progress_style': "100%"
            })
        
        # Rule 2: Savings > ₹10,000 Threshold for SIP/FD
        if total_savings > 10000:
            # SIP Suggestion
            sip_recommendation = {
                'priority': 2,
                'title': '📈 Systematic Investment Plan (SIP)',
                'description': 'Regular mutual fund investment for long-term growth.',
                'type': 'SIP',
                'suggested_amount': total_savings * 0.20,
                'reason': 'Rupee-cost averaging helps in wealth building over 5+ years.',
                'details': [
                    '• Suggested: 15-20% of savings',
                    f'• Amount: ₹{total_savings * 0.20:.2f}',
                    '• Risk: Moderate'
                ]
            }
            recommendations.append(sip_recommendation)
            
            # FD Suggestion
            fd_recommendation = {
                'priority': 2,
                'title': '🏦 Fixed Deposit (FD)',
                'description': 'Safe investment with guaranteed returns.',
                'type': 'FD',
                'suggested_amount': total_savings * 0.15,
                'reason': 'FDs provide stability and guaranteed interest.',
                'details': [
                    '• Suggested: 10-15% of savings',
                    f'• Amount: ₹{total_savings * 0.15:.2f}',
                    '• Risk: Very Low'
                ]
            }
            recommendations.append(fd_recommendation)

            # Rule 3: Stocks (Only if Emergency Fund is Secure)
            if emergency_fund_is_secure:
                recommendations.append({
                    'priority': 3,
                    'title': '📊 Stocks / Direct Equity',
                    'description': 'High-growth potential for 5+ years.',
                    'type': 'Stocks',
                    'suggested_amount': total_savings * 0.10,
                    'reason': 'Equity yields high returns over long periods.',
                    'details': [
                        '• Suggested: 5-10% allocation',
                        f'• Amount: ₹{total_savings * 0.10:.2f}'
                    ]
                })
        else:
            # Advice for low savings
            recommendations.append({
                'priority': 1,
                'title': '💰 Increase Savings',
                'description': f'You have ₹{total_savings:.2f} in savings.',
                'action': f'Save ₹{10000 - total_savings:.2f} more to unlock SIP and FD recommendations.',
                'reason': 'A minimum threshold of ₹10,000 is recommended before starting dedicated investment plans.'
            })
        
        # Rule 4: Gold (Always a good hedge)
        if total_savings > 5000:
            recommendations.append({
                'priority': 3,
                'title': '🏆 Gold Investment',
                'description': 'Inflation hedge and asset protection.',
                'type': 'Gold',
                'suggested_amount': total_savings * 0.05,
                'reason': 'Gold maintains value during market volatility.',
                'details': [f'• Suggested: ₹{total_savings * 0.05:.2f} (3-5%)']
            })
        
        # Suggested allocation summary
        if total_savings > 10000:
            allocation = {
                'priority': 0,
                'title': '💡 Suggested Investment Allocation',
                'description': f'Strategy for your ₹{total_savings:.2f} savings',
                'allocation': {
                    'Emergency Fund': max(0, emergency_fund_needed - current_emergency_fund),
                    'SIP (Mutual Funds)': total_savings * 0.20,
                    'Fixed Deposit': total_savings * 0.15,
                    'Stocks': total_savings * 0.10 if emergency_fund_is_secure else 0,
                    'Gold': total_savings * 0.05,
                    'Liquid Cash': total_savings * 0.15
                }
            }
            recommendations.insert(0, allocation)

        elif total_savings == 0:
            recommendations.append({
                'priority': 1,
                'title': '💰 Start Saving!',
                'description': 'No savings recorded yet',
                'action': 'Begin by saving ₹5,000-10,000 monthly to build a strong financial foundation',
                'reason': 'Consistent savings are the foundation of wealth building.'
            })
        else:
            recommendations.append({
                'priority': 1,
                'title': '📈 Keep Saving',
                'description': f'You have ₹{total_savings:.2f} saved',
                'action': f'Target to reach ₹10,000 to unlock SIP and FD recommendations',
                'reason': 'You need ₹{:.2f} more to start investing in SIPs and FDs'.format(10000 - total_savings),
                'current': total_savings,
                'required': 10000,
                'progress_pct': (total_savings / 10000) * 100,
                'progress_style': f"{(total_savings / 10000) * 100:.1f}%"
            })
        
        return {
            'summary': summary,
            'recommendations': sorted(recommendations, key=lambda x: x['priority'])
        }
    
    @staticmethod
    def get_monthly_expense_average(user_id, months=3):
        """Calculate average monthly expenses for last N months"""
        total_expense = 0
        
        for i in range(months):
            month_start = datetime.utcnow().replace(day=1) - timedelta(days=i*30)
            month_end = month_start + timedelta(days=32)
            
            month_expense = db.session.query(func.sum(Expense.amount)).filter(
                Expense.user_id == user_id,
                Expense.date >= month_start.replace(day=1),
                Expense.date < month_end.replace(day=1)
            ).scalar() or 0
            
            total_expense += month_expense
        
        return total_expense / months if months > 0 else 0
