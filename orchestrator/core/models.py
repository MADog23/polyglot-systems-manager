"""
Pydantic models used throughout the Polyglot Orchestrator.

These models define the validated structure for:
- Individual service configuration
- Top-level orchestrator configuration
"""

from pydantic import BaseModel, Field
from typing import List, Optional


class ServiceConfig(BaseModel):
    """
    Configuration for a single managed service.
    """
    name: str = Field(..., description="Human-readable service name")
    command: List[str] = Field(..., description="Command used to start the service")
    healthcheck_url: Optional[str] = Field(
        None, description="HTTP URL used to check service health"
    )
    restart: str = Field(
        "always",
        description="Restart policy: 'always', 'on-failure', or 'never'"
    )


class OrchestratorConfig(BaseModel):
    """
    Top-level orchestrator configuration.
    """
    services: List[ServiceConfig] = Field(
        ..., description="List of services managed by the orchestrator"
    )
    healthcheck_interval: float = Field(
        2.0,
        description="Seconds between orchestrator health checks"
    )
