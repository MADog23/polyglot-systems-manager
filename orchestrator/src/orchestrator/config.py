from typing import List, Optional
from pydantic import BaseModel


class ServiceConfig(BaseModel):
    """
    Configuration for a single managed service.

    Attributes
    ----------
    name : str
        Human-readable name of the service.
    command : List[str]
        The command used to launch the service as a subprocess.
    healthcheck_url : Optional[str]
        Optional URL used for HTTP health-check probing.
    restart : str
        Restart policy: "always", "on-failure", or "never".
    max_restarts : int
        Maximum number of restarts allowed within the restart window.
    restart_window_seconds : int
        Time window (in seconds) for counting restarts.
    """

    name: str
    command: List[str]
    healthcheck_url: Optional[str] = None  # URL for HTTP health checks

    # Intermediate restart policy configuration
    restart: str = "always"               # "always", "on-failure", "never"
    max_restarts: int = 3                 # Max restarts allowed in window
    restart_window_seconds: int = 60      # Window for counting restarts


class OrchestratorConfig(BaseModel):
    """
    Top-level configuration for the orchestrator.

    Attributes
    ----------
    services : List[ServiceConfig]
        List of services the orchestrator should manage.
    poll_interval_seconds : int
        How often the orchestrator prints status and performs checks.
    """

    services: List[ServiceConfig]
    poll_interval_seconds: int = 5
