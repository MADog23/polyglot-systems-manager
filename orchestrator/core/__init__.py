"""
Core package for the Polyglot Orchestrator.

This package contains:
- Orchestrator control loop
- Service process management
- Configuration loading
- Pydantic models for configuration schema
"""

from .orchestrator import Orchestrator
from .config import load_config_from_yaml
from .service_process import ServiceProcess
from .models import OrchestratorConfig, ServiceConfig
