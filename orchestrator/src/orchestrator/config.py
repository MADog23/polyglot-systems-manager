from typing import List, Optional
from pydantic import BaseModel


class ServiceConfig(BaseModel):
    name: str                       # Human-readable name
    command: List[str]              # Command to launch the service
    healthcheck_url: Optional[str] = None   # Future: health checks


class OrchestratorConfig(BaseModel):
    services: List[ServiceConfig]   # List of services to manage
    poll_interval_seconds: int = 5  # How often to check status
