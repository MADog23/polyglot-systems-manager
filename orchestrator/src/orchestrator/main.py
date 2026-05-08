import subprocess
import time
from typing import List

from .config import OrchestratorConfig, ServiceConfig


class ServiceProcess:
    """
    Wrapper around a subprocess representing a managed service.

    This class abstracts:
    - starting the service
    - stopping it gracefully
    - checking whether it is still running

    Parameters
    ----------
    config : ServiceConfig
        The configuration describing how to launch the service.
    """

    def __init__(self, config: ServiceConfig):
        self.config = config
        self.process: subprocess.Popen | None = None  # Will hold the running subprocess

    def start(self) -> None:
        """
        Start the service if it is not already running.

        Launches the subprocess using the command defined in the
        ServiceConfig. If the service is already running, this method
        does nothing.
        """

        # If the process exists AND hasn't exited, it's already running.
        if self.process is not None and self.process.poll() is None:
            print(f"[{self.config.name}] already running")
            return

        # Launch the service as a subprocess.
        # Popen returns immediately, allowing the orchestrator to continue running.
        print(f"[{self.config.name}] starting: {' '.join(self.config.command)}")
        self.process = subprocess.Popen(self.config.command)

    def stop(self) -> None:
        """
        Stop the service gracefully.

        Attempts to terminate the subprocess. If the process does not
        exit within a timeout, it is force‑killed.
        """

        # If the process was never started, nothing to stop.
        if self.process is None:
            print(f"[{self.config.name}] not running")
            return

        print(f"[{self.config.name}] stopping")
        self.process.terminate()  # Ask the process to exit cleanly

        try:
            # Wait up to 5 seconds for graceful shutdown.
            self.process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            # If the process refuses to exit, force-kill it.
            print(f"[{self.config.name}] did not exit, killing")
            self.process.kill()

    def is_running(self) -> bool:
        """
        Check whether the service process is still alive.

        Returns
        -------
        bool
            True if the subprocess is running, False otherwise.
        """

        # poll() returns None when the process is still alive.
        return self.process is not None and self.process.poll() is None


class Orchestrator:
    """
    Main orchestrator responsible for managing multiple services.

    Responsibilities
    ----------------
    - Start all configured services
    - Periodically report their status
    - Shut down all services on exit
    """

    def __init__(self, config: OrchestratorConfig):
        """
        Initialize the orchestrator with a configuration.

        Parameters
        ----------
        config : OrchestratorConfig
            The configuration describing all services to manage.
        """

        self.config = config

        # Convert each ServiceConfig into a ServiceProcess instance.
        # This separates configuration from runtime behavior.
        self.services: List[ServiceProcess] = [
            ServiceProcess(svc) for svc in config.services
        ]

    def start_all(self) -> None:
        """
        Start all services defined in the configuration.
        """

        # Start each service in sequence.
        # In the future, this could be parallelized if needed.
        for svc in self.services:
            svc.start()

    def stop_all(self) -> None:
        """
        Stop all running services gracefully.
        """

        # Stop services in the order they were started.
        # If dependencies matter later, we can reverse this order.
        for svc in self.services:
            svc.stop()

    def run(self) -> None:
        """
        Run the orchestrator's main control loop.

        Behavior
        --------
        - Starts all services
        - Enters a periodic status loop
        - Handles Ctrl+C (KeyboardInterrupt) for clean shutdown
        """

        try:
            # Start all configured services.
            self.start_all()
            print("[orchestrator] all services started")

            # Main control loop:
            # - Check which services are still running
            # - Print status every poll interval
            while True:
                running = [svc for svc in self.services if svc.is_running()]
                print(f"[orchestrator] {len(running)}/{len(self.services)} services running")

                # Sleep between status checks.
                time.sleep(self.config.poll_interval_seconds)

        except KeyboardInterrupt:
            # Ctrl+C triggers a clean shutdown.
            print("\n[orchestrator] received KeyboardInterrupt, shutting down")

        finally:
            # Ensure all services are stopped even if an error occurs.
            self.stop_all()


def build_default_config() -> OrchestratorConfig:
    """
    Build a temporary default configuration using placeholder services.

    These placeholder services run simple Python HTTP servers so the
    orchestrator can demonstrate process management before integrating
    real C++, Java, and Node.js components.

    Returns
    -------
    OrchestratorConfig
        A configuration object containing three placeholder services.
    """

    # Temporary placeholder services.
    # Each one runs a simple Python HTTP server so the orchestrator
    # can demonstrate process management before real services exist.
    return OrchestratorConfig(
        services=[
            ServiceConfig(
                name="metrics-collector",
                command=["python", "-m", "http.server", "8001"],
            ),
            ServiceConfig(
                name="java-service",
                command=["python", "-m", "http.server", "8002"],
            ),
            ServiceConfig(
                name="node-api",
                command=["python", "-m", "http.server", "8003"],
            ),
        ],
        poll_interval_seconds=5,
    )


def main() -> None:
    """
    Entry point for the orchestrator CLI.

    Loads the default configuration, constructs the orchestrator,
    and starts the main control loop.
    """

    # Build the default config and start the orchestrator.
    config = build_default_config()
    orchestrator = Orchestrator(config)
    orchestrator.run()


if __name__ == "__main__":
    main()
