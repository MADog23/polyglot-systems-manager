import subprocess
import time
import urllib.request
import yaml
from typing import List
import os
from flask import Flask, send_from_directory, jsonify
import requests
from .config import OrchestratorConfig, ServiceConfig

# -----------------------------
# Orchestrator policy constants
# -----------------------------

WARMUP_GRACE_SECONDS = 5      # time after (re)start before we judge health
MIN_RESTART_INTERVAL = 5      # minimum seconds between restarts
MAX_RESTARTS = 5              # safety cap (used only if config doesn't override)


def load_config_from_yaml(path: str) -> OrchestratorConfig:
    """
    Load orchestrator configuration from a YAML file and validate it
    using Pydantic models.
    """
    with open(path, "r") as f:
        raw = yaml.safe_load(f)
    return OrchestratorConfig(**raw)


class ServiceProcess:
    """
    Wrapper around a subprocess representing a managed service.
    """

    def __init__(self, config: ServiceConfig):
        self.config = config
        self.process: subprocess.Popen | None = None

        # Restart tracking
        self.restart_count: int = 0
        self.last_restart_time: float = 0.0

        # Warm-up tracking
        self.start_time: float = 0.0

    def start(self) -> None:
        """Start the service if not already running."""
        if self.process is not None and self.process.poll() is None:
            print(f"[{self.config.name}] already running")
            return

        print(f"[{self.config.name}] starting: {' '.join(self.config.command)}")
        self.process = subprocess.Popen(self.config.command)
        self.start_time = time.time()   # <-- NEW

    def stop(self) -> None:
        """Stop the service gracefully."""
        if self.process is None:
            print(f"[{self.config.name}] not running")
            return

        print(f"[{self.config.name}] stopping")
        self.process.terminate()

        try:
            self.process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            print(f"[{self.config.name}] did not exit, killing")
            self.process.kill()

    def is_running(self) -> bool:
        """Return True if the subprocess is alive."""
        return self.process is not None and self.process.poll() is None

    def is_healthy(self) -> bool:
        """Perform an HTTP GET health check."""
        if not self.config.healthcheck_url:
            return True

        try:
            with urllib.request.urlopen(self.config.healthcheck_url, timeout=2) as resp:
                if resp.status != 200:
                    return False
        except Exception:
            return False

        # Optional: metrics endpoint check (but do NOT fail on zero values)
        if "metrics" in self.config.name.lower():
            try:
                metrics_url = self.config.healthcheck_url.replace("health", "metrics")
                with urllib.request.urlopen(metrics_url, timeout=2):
                    pass  # reachable = healthy
            except Exception:
                return False

        return True

    def should_restart(self, healthy: bool) -> bool:
        """
        Determine whether the service should be restarted based on
        restart policy and restart limits.
        """
        policy = self.config.restart

        if policy == "never":
            return False
        if policy == "on-failure" and healthy:
            return False

        now = time.time()

        # Reset restart window if enough time has passed
        if now - self.last_restart_time > self.config.restart_window_seconds:
            self.restart_count = 0

        if self.restart_count >= self.config.max_restarts:
            print(
                f"[{self.config.name}] restart limit reached: "
                f"{self.restart_count}/{self.config.max_restarts}"
            )
            return False

        return True

    def record_restart(self) -> None:
        """Record a restart event."""
        self.restart_count += 1
        self.last_restart_time = time.time()


class Orchestrator:
    """
    Main orchestrator responsible for managing multiple services.
    """

    def __init__(self, config: OrchestratorConfig):
        self.config = config
        self.services: List[ServiceProcess] = [
            ServiceProcess(svc) for svc in config.services
        ]

    def start_all(self) -> None:
        """Start all configured services."""
        for svc in self.services:
            svc.start()

    def stop_all(self) -> None:
        """Stop all running services."""
        for svc in self.services:
            svc.stop()

    def run(self) -> None:
        """Run the orchestrator's main control loop."""
        try:
            self.start_all()
            print("[orchestrator] all services started")

            while True:
                running_count = 0
                healthy_count = 0

                for svc in self.services:
                    running = svc.is_running()

                    # -----------------------------
                    # Warm-up grace period
                    # -----------------------------
                    if running and (time.time() - svc.start_time < WARMUP_GRACE_SECONDS):
                        healthy = True
                    else:
                        healthy = svc.is_healthy() if running else False

                    if running:
                        running_count += 1
                    if healthy:
                        healthy_count += 1

                    # -----------------------------
                    # Restart logic with backoff
                    # -----------------------------
                    if (not running) or (running and not healthy):
                        reason = "not running" if not running else "unhealthy"

                        if svc.should_restart(healthy):
                            now = time.time()

                            # Restart backoff
                            if now - svc.last_restart_time < MIN_RESTART_INTERVAL:
                                wait = MIN_RESTART_INTERVAL - (now - svc.last_restart_time)
                                print(
                                    f"[{svc.config.name}] restart_backoff "
                                    f"waiting={wait:.1f}s"
                                )
                                continue

                            print(f"[{svc.config.name}] restarting ({reason})")
                            print(
                                f"[{svc.config.name}] restart_triggered "
                                f"reason={reason} "
                                f"restart_count={svc.restart_count + 1}/"
                                f"{svc.config.max_restarts} "
                                f"policy={svc.config.restart}"
                            )

                            svc.stop()
                            svc.start()
                            svc.record_restart()
                        else:
                            print(
                                f"[{svc.config.name}] restart_skipped "
                                f"reason={reason} "
                                f"restart_count={svc.restart_count}/"
                                f"{svc.config.max_restarts} "
                                f"policy={svc.config.restart}"
                            )

                print(
                    f"[orchestrator] {running_count}/{len(self.services)} running, "
                    f"{healthy_count} healthy"
                )

                time.sleep(self.config.poll_interval_seconds)

        except KeyboardInterrupt:
            print("\n[orchestrator] received KeyboardInterrupt, shutting down")

        finally:
            self.stop_all()


def main() -> None:
    # -------------------------------
    # Flask Dashboard Server
    # -------------------------------
    app = Flask(__name__, static_folder="dashboard")

    DASHBOARD_DIR = os.path.join(os.path.dirname(__file__), "dashboard")
    COLLECTOR_URL = "http://localhost:9001/metrics"

    @app.route("/dashboard")
    def dashboard():
        return send_from_directory(DASHBOARD_DIR, "index.html")

    @app.route("/dashboard/<path:path>")
    def dashboard_static(path):
        return send_from_directory(DASHBOARD_DIR, path)

    @app.route("/api/metrics")
    def api_metrics():
        try:
            r = requests.get(COLLECTOR_URL, timeout=1)
            return jsonify(r.json())
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route("/")
    def root():
        return dashboard()

    # -------------------------------
    # Start Flask in background thread
    # -------------------------------
    import threading

    def run_flask():
        print("Dashboard available at http://localhost:8000/dashboard")
        app.run(port=8000, debug=False, use_reloader=False)

    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()

    # -------------------------------
    # Start Orchestrator
    # -------------------------------
    base_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.normpath(os.path.join(base_dir, "..", "..", "config.yaml"))

    print(f"[orchestrator] loading config from: {config_path}")

    config = load_config_from_yaml(config_path)
    orchestrator = Orchestrator(config)
    orchestrator.run()   # <-- this now executes!


if __name__ == "__main__":
    main()
