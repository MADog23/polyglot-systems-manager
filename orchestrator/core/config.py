"""
Configuration loading and schema definitions for the Polyglot Orchestrator.

This module:
- Defines Pydantic models for orchestrator + service configuration
- Loads and validates config.yaml from disk
- Provides a clean API for the orchestrator to consume configuration
"""

import yaml
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


def load_config_from_yaml(path: str) -> OrchestratorConfig:
    """
    Load and validate orchestrator configuration from a YAML file.

    Parameters
    ----------
    path : str
        Path to the config.yaml file.

    Returns
    -------
    OrchestratorConfig
        Parsed and validated configuration object.
    """
    with open(path, "r", encoding="utf-8") as f:
        raw = yaml.safe_load(f)

    return OrchestratorConfig(**raw)
