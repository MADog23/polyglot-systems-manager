"""
Core orchestrator control loop for the Polyglot Systems Manager.

This module:
- Starts and supervises all configured services
- Performs periodic health checks
- Applies restart policies
- Tracks service state and restart counts
"""

import time
import requests
from typing import List

from .models import OrchestratorConfig, ServiceConfig
from .service_process import ServiceProcess


class Orchestrator:
    """
    The orchestrator is the control plane responsible for:
    - launching services
    - monitoring health
    - restarting failed services
    - enforcing restart policies
    """

    def __init__(self, config: OrchestratorConfig) -> None:
        self.config = config
        self.services: List[ServiceProcess] = []

        # Convert config entries into ServiceProcess objects
        for svc_cfg in config.services:
            self.services.append(ServiceProcess(svc_cfg))

    # ----------------------------------------------------------------------
    # Service Lifecycle
    # ----------------------------------------------------------------------

    def start_all(self) -> None:
        """Start all configured services."""
        print("[orchestrator] starting services...")
        for svc in self.services:
            svc.start()

    def stop_all(self) -> None:
        """Stop all services gracefully."""
        print("[orchestrator] stopping services...")
        for svc in self.services:
            svc.stop()

    # ----------------------------------------------------------------------
    # Health Checking
    # ----------------------------------------------------------------------

    def check_service_health(self, svc: ServiceProcess) -> bool:
        """
        Perform a health check for a single service.

        Returns True if healthy, False otherwise.
        """
        # If the process is not running, it's unhealthy
        if not svc.is_running():
            return False

        # If no healthcheck URL is defined, assume healthy
        if not svc.config.healthcheck_url:
            return True

        try:
            r = requests.get(svc.config.healthcheck_url, timeout=1.0)
            return r.status_code == 200
        except Exception:
            return False

    # ----------------------------------------------------------------------
    # Restart Policy
    # ----------------------------------------------------------------------

    def apply_restart_policy(self, svc: ServiceProcess, healthy: bool) -> None:
        """
        Apply restart policy based on service health.
        """
        if healthy:
            return

        policy = svc.config.restart

        if policy == "never":
            return

        if policy == "on-failure" and svc.is_running():
            # Process is running but unhealthy → restart
            print(f"[orchestrator] restarting unhealthy service: {svc.config.name}")
            svc.restart()
            return

        if policy == "always":
            print(f"[orchestrator] restarting service (policy=always): {svc.config.name}")
            svc.restart()
            return

    # ----------------------------------------------------------------------
    # Main Control Loop
    # ----------------------------------------------------------------------

    def run(self) -> None:
        """
        Main orchestrator loop.
        Runs indefinitely, performing health checks and applying restart policies.
        """
        self.start_all()

        interval = self.config.healthcheck_interval

        print("[orchestrator] entering control loop")
        while True:
            for svc in self.services:
                healthy = self.check_service_health(svc)
                svc.last_health = healthy

                if not healthy:
                    print(f"[orchestrator] service unhealthy: {svc.config.name}")

                self.apply_restart_policy(svc, healthy)

            time.sleep(interval)
