"""
Server package for the Polyglot Orchestrator.

This package contains:
- Flask app factory
- API routes for metrics and service status
- Dashboard static file serving
"""

from .app import create_app
