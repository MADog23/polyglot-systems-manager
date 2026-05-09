"""
API route definitions for the Polyglot Orchestrator.

These routes are registered by the Flask app factory in app.py.
They provide:
- Service status information
- Metrics proxying from the C++ collector
"""

from flask import Blueprint, jsonify
import requests

routes = Blueprint("routes", __name__)


def register_routes(app, orchestrator):
    """
    Register all API routes onto the given Flask app.

    Parameters
    ----------
    app : Flask
        The Flask application instance.
    orchestrator : Orchestrator
        The orchestrator instance managing all services.
    """

    @app.route("/api/services")
    def api_services():
        """Return status information for all managed services."""
        data = []
        for svc in orchestrator.services:
            data.append({
                "name": svc.config.name,
                "running": svc.is_running(),
                "healthy": svc.last_health,
                "restarts": svc.restart_count
            })
        return jsonify(data)

    @app.route("/api/metrics")
    def api_metrics():
        """
        Proxy metrics from the C++ collector.
        Assumes the collector exposes /metrics on port 9001.
        """
        try:
            r = requests.get("http://localhost:9001/metrics", timeout=1.0)
            return jsonify(r.json())
        except Exception as e:
            return jsonify({"error": str(e)}), 500
