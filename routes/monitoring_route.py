from flask import Blueprint, jsonify
from services.monitoring_service import get_dashboard_stats, get_account_health, get_recent_logs

monitoring_bp = Blueprint("monitoring", __name__)

@monitoring_bp.route("/monitoring", methods=["GET"])
def monitoring():
    stats = get_dashboard_stats()
    accounts = get_account_health()
    logs = get_recent_logs()
    
    return jsonify({
        "status": "online",
        "stats": stats,
        "accounts": accounts,
        "recent_logs": logs
    })
