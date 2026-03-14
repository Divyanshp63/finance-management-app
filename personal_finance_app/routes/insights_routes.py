from flask import Blueprint, render_template, jsonify
from flask_login import login_required, current_user
from services.insights_service import InsightsService
from services.prediction_service import PredictionService
from services.alerts_service import AlertsService

insights_bp = Blueprint("insights", __name__, url_prefix="/insights")

@insights_bp.route("/")
@login_required
def insights():
    insights = InsightsService.get_all_insights(current_user.id)
    predictions = PredictionService.get_all_predictions(current_user.id)
    alerts = AlertsService.get_all_alerts(current_user.id)
    
    return render_template("insights.html", 
                          insights=insights, 
                          predictions=predictions,
                          alerts=alerts)

@insights_bp.route("/api/insights")
@login_required
def api_insights():
    insights = InsightsService.get_all_insights(current_user.id)
    return jsonify(insights)

@insights_bp.route("/api/predictions")
@login_required
def api_predictions():
    predictions = PredictionService.get_all_predictions(current_user.id)
    return jsonify(predictions)

@insights_bp.route("/api/alerts")
@login_required
def api_alerts():
    alerts = AlertsService.get_all_alerts(current_user.id)
    return jsonify(alerts)

@insights_bp.route("/api/spending-trend")
@login_required
def api_spending_trend():
    trend = InsightsService.get_spending_trend(current_user.id)
    return jsonify(trend) if trend else jsonify({'error': 'No data'}), 404

@insights_bp.route("/api/category-forecast")
@login_required
def api_category_forecast():
    forecast = PredictionService.get_category_forecast(current_user.id)
    return jsonify(forecast)
