import subprocess
import time
from typing import List

from .config import OrchestratorConfig, ServiceConfig


class ServiceProcess:
    def __init__(self, config: ServiceConfig):
        self.config = config
        self.process: subprocess.Popen | None = None

    def start(self) -> None:
        # Starts a subprocess for the service
        # Uses Popen so the orchestrator can monitor it
        if self.process is not None and self.process.poll() is None:
            print(f"[{self.config.name}] already running")
            return
        print(f"[{self.config.name}] starting: {' '.join(self.config.command)}")
        self.process = subprocess.Popen(self.config.command)

    def stop(self) -> None:
        # Gracefully terminates the service
        # Falls back to kill() if needed
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
        # Checks if the process is still alive
        return self.process is not None and self.process.poll() is None


class Orchestrator:
    def __init__(self, config: OrchestratorConfig):
        self.config = config
        self.services: List[ServiceProcess] = [
            ServiceProcess(svc) for svc in config.services
        ]

    def start_all(self) -> None:
        # Starts every service defined in the config
        for svc in self.services:
            svc.start()

    def stop_all(self) -> None:
        for svc in self.services:
            svc.stop()

    def run(self) -> None:
        # Main loop:
            # 1. Start all services
            # 2. Periodically check their status
            # 3. Shutdown cleanly on Ctrl+C
        try:
            self.start_all()
            print("[orchestrator] all services started")
            while True:
                running = [svc for svc in self.services if svc.is_running()]
                print(f"[orchestrator] {len(running)}/{len(self.services)} services running")
                time.sleep(self.config.poll_interval_seconds)
        except KeyboardInterrupt:
            print("\n[orchestrator] received KeyboardInterrupt, shutting down")
        finally:
            self.stop_all()


def build_default_config() -> OrchestratorConfig:
    # Temporary placeholder services
    # These will be replaced with real C++, Java, Node services
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
    config = build_default_config()
    orchestrator = Orchestrator(config)
    orchestrator.run()


if __name__ == "__main__":
    main()
