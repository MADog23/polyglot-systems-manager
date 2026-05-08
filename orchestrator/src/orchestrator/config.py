from typing import List, Optional
from pydantic import BaseModel


class ServiceConfig(BaseModel):
    """
    Configuration for a single managed service.

    Attributes
    ----------
    name : str
        Human‑readable name of the service.
    command : List[str]
        The command used to launch the service as a subprocess.
    healthcheck_url : Optional[str]
        Optional URL used for future health‑check probing.
    """

    # Represents a single service the orchestrator will manage.
    # Each service is launched as a subprocess using the given command.
    name: str
    command: List[str]
    healthcheck_url: Optional[str] = None  # Reserved for future health checks


class OrchestratorConfig(BaseModel):
    """
    Top‑level configuration for the orchestrator.

    Attributes
    ----------
    services : List[ServiceConfig]
        List of services the orchestrator should manage.
    poll_interval_seconds : int
        How often the orchestrator prints status and performs checks.
    """

    services: List[ServiceConfig]
    poll_interval_seconds: int = 5     # controls how often the orchestrator prints status.

