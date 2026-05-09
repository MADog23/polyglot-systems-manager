"""
Flask application factory for the Polyglot Orchestrator.

This module creates the Flask app responsible for:
- Serving the dashboard UI from /web
- Exposing API endpoints for service status and metrics
- Integrating with the orchestrator instance passed in at startup
"""

import os
from flask import Flask, send_from_directory, jsonify
import requests


def create_app(orchestrator) -> Flask:
    """
    Create and configure the Flask application.

    Parameters
    ----------
    orchestrator : Orchestrator
        The orchestrator instance that manages all services.

    Returns
    -------
    Flask
        Configured Flask application.
    """
    app = Flask(__name__)

    # Resolve the absolute path to the /web directory
    WEB_DIR = os.path.normpath(
        os.path.join(os.path.dirname(__file__), "..", "..", "web")
    )

    # ------------------------------------------------------------
    # Static file routes (CSS, JS, images)
    # ------------------------------------------------------------
    @app.route("/css/<path:filename>")
    def css(filename):
        return send_from_directory(os.path.join(WEB_DIR, "css"), filename)

    @app.route("/js/<path:filename>")
    def js(filename):
        return send_from_directory(os.path.join(WEB_DIR, "js"), filename)

    # ------------------------------------------------------------------
    # Dashboard Routes
    # ------------------------------------------------------------------

    @app.route("/dashboard")
    def dashboard():
        """Serve the main dashboard HTML page."""
        return send_from_directory(WEB_DIR, "index.html")

    @app.route("/dashboard/<path:path>")
    def dashboard_static(path):
        """Serve JS, CSS, and other static dashboard assets."""
        return send_from_directory(WEB_DIR, path)

    # ------------------------------------------------------------------
    # API Routes
    # ------------------------------------------------------------------

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

    # Root → redirect to dashboard
    @app.route("/")
    def root():
        return dashboard()

    return app
