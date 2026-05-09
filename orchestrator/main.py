"""
Entry point for the Polyglot Systems Manager orchestrator.

- Loads system configuration from the repo root (config.yaml)
- Constructs the Orchestrator control plane
- Creates the Flask dashboard/server
- Runs Flask in a background thread
- Runs the orchestrator control loop in the main thread
"""

import os
import threading

from core.orchestrator import Orchestrator
from core.config import load_config_from_yaml
from server.app import create_app


def main() -> None:
    """
    Main entrypoint for the orchestrator CLI.
    Wires together configuration, orchestrator core, and the HTTP dashboard server.
    """
    # Resolve repo root and config path
    base_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.normpath(os.path.join(base_dir, "..", "config.yaml"))

    print(f"[orchestrator] loading config from: {config_path}")
    config = load_config_from_yaml(config_path)

    # Create orchestrator control plane
    orchestrator = Orchestrator(config)

    # Create Flask app bound to this orchestrator instance
    app = create_app(orchestrator)

    # Run Flask dashboard in a background thread
    def run_flask() -> None:
        print("[orchestrator] dashboard available at http://localhost:8000/dashboard")
        # debug=False + use_reloader=False to avoid double processes
        app.run(port=8000, debug=False, use_reloader=False)

    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()

    # Run orchestrator control loop in the main thread
    orchestrator.run()


if __name__ == "__main__":
    main()
