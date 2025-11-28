from flask import Blueprint, jsonify
from services.monitoring_service import run_monitoring

monitoring_bp = Blueprint("monitoring", __name__)

@monitoring_bp.route("/monitoring", methods=["GET"])
def monitoring():
    results = run_monitoring()
    return jsonify({"status": "completed", "results": results})
