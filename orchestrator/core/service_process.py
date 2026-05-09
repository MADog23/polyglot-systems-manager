"""
ServiceProcess: A subprocess wrapper used by the Polyglot Orchestrator.

This class is responsible for:
- launching a service as a subprocess
- tracking its running state
- performing restarts
- capturing restart counts
- stopping the service cleanly
"""

import subprocess
import time
from typing import Optional

from .models import ServiceConfig


class ServiceProcess:
    """
    Wraps a single managed service process.

    Each service is defined by a ServiceConfig and managed by:
    - start()
    - stop()
    - restart()
    - is_running()
    """

    def __init__(self, config: ServiceConfig) -> None:
        self.config = config
        self.process: Optional[subprocess.Popen] = None
        self.restart_count: int = 0
        self.last_health: Optional[bool] = None

    # ------------------------------------------------------------------
    # Process Lifecycle
    # ------------------------------------------------------------------

    def start(self) -> None:
        """Start the service as a subprocess."""
        if self.process and self.is_running():
            print(f"[service:{self.config.name}] already running")
            return

        print(f"[service:{self.config.name}] starting: {' '.join(self.config.command)}")

        try:
            self.process = subprocess.Popen(
                self.config.command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
        except Exception as e:
            print(f"[service:{self.config.name}] failed to start: {e}")
            self.process = None

    def stop(self) -> None:
        """Stop the service gracefully."""
        if not self.process:
            return

        print(f"[service:{self.config.name}] stopping...")

        try:
            self.process.terminate()
            self.process.wait(timeout=5)
        except Exception:
            print(f"[service:{self.config.name}] force killing...")
            self.process.kill()

        self.process = None

    def restart(self) -> None:
        """Restart the service."""
        print(f"[service:{self.config.name}] restarting...")
        self.stop()
        time.sleep(0.5)
        self.start()
        self.restart_count += 1

    # ------------------------------------------------------------------
    # State Inspection
    # ------------------------------------------------------------------

    def is_running(self) -> bool:
        """Return True if the subprocess is alive."""
        if not self.process:
            return False
        return self.process.poll() is None
