import sys
import os

# Add the app directory to sys.path
sys.path.append(r'c:\Users\Divya\OneDrive\Desktop\personal_finance_app')

from services.investment_advisor import InvestmentAdvisor
from unittest.mock import MagicMock

def test_logic():
    print("Testing Investment Advisor Logic...")
    
    # Case 1: Low Savings (< 10,000)
    print("\nCase 1: Savings = 5,000 (Low Savings)")
    mock_summary = {
        'total_savings': 5000,
        'monthly_expenses': 2000,
        'total_investments': 0,
        'investment_breakdown': {}
    }
    InvestmentAdvisor.get_user_summary = MagicMock(return_value=mock_summary)
    result = InvestmentAdvisor.get_recommendations(1)
    
    titles = [r['title'] for r in result['recommendations']]
    print(f"Titles: {titles}")
    assert "💰 Increase Savings" in titles
    assert "📈 Systematic Investment Plan (SIP)" not in titles
    
    # Case 2: High Savings but No Emergency Fund
    print("\nCase 2: Savings = 15,000, No Emergency Fund")
    mock_summary = {
        'total_savings': 15000,
        'monthly_expenses': 4000, # Needs 12k
        'total_investments': 0,
        'investment_breakdown': {}
    }
    InvestmentAdvisor.get_user_summary = MagicMock(return_value=mock_summary)
    result = InvestmentAdvisor.get_recommendations(1)
    
    titles = [r['title'] for r in result['recommendations']]
    print(f"Titles: {titles}")
    assert "🚨 Build Emergency Fund (Top Priority)" in titles
    assert "📈 Systematic Investment Plan (SIP)" in titles # Triggered by >10k
    assert "📊 Stocks / Direct Equity" not in titles # Should be blocked by emergency fund
    
    # Case 3: High Savings + Secure Emergency Fund
    print("\nCase 3: Savings = 20,000, Secure Emergency Fund")
    mock_summary = {
        'total_savings': 20000,
        'monthly_expenses': 3000, # Needs 9k
        'total_investments': 10000,
        'investment_breakdown': {'Emergency Fund': 10000}
    }
    InvestmentAdvisor.get_user_summary = MagicMock(return_value=mock_summary)
    result = InvestmentAdvisor.get_recommendations(1)
    
    titles = [r['title'] for r in result['recommendations']]
    print(f"Titles: {titles}")
    assert "✅ Emergency Fund Secure" in titles
    assert "📈 Systematic Investment Plan (SIP)" in titles
    assert "📊 Stocks / Direct Equity" in titles # Now available

    print("\nAll logic tests passed!")

if __name__ == "__main__":
    test_logic()
