# Polyglot Orchestrator

## Overview
The **Polyglot Orchestrator** is the Python-based control plane for the **Polyglot Systems Monitor (PSM)**.  
Its job is to start, monitor, and gracefully shut down multiple heterogeneous services written in different languages (C++, Java, Node.js, Python).

This orchestrator acts as the “systemd/Kubernetes-lite” for the entire project.

---

## Features
- Launches multiple services as subprocesses  
- Monitors service liveness  
- Gracefully terminates all services on shutdown  
- Typed configuration using Pydantic  
- CLI entrypoint: `psm-orchestrator`  
- Extensible architecture for:
  - health checks  
  - restart policies  
  - log capture  
  - YAML/JSON config files  

---

## Architecture

### Components
| Component | Description |
|----------|-------------|
| ServiceConfig | Defines how a service should be launched |
| ServiceProcess | Wraps a subprocess and manages its lifecycle |
| Orchestrator | Starts, monitors, and stops all services |
| CLI Entrypoint | Runs the orchestrator via `psm-orchestrator` |

### Runtime Flow
1. Load configuration  
2. Convert each service into a `ServiceProcess`  
3. Start all services  
4. Enter monitoring loop  
5. On Ctrl+C → gracefully shut down all services  

---

## Directory Structure

```
orchestrator/
│── pyproject.toml
│── README.md
│── src/
│   └── orchestrator/
│       ├── __init__.py
│       ├── config.py
│       └── main.py
│── tests/
```

---

## Installation

### 1. Create and activate a virtual environment
```
py -3.12 -m venv .venv
.venv\Scripts\activate
```

### 2. Install the orchestrator in editable mode
```
pip install -e .
```

---

## Running the Orchestrator

### Option 1 — CLI entrypoint
```
psm-orchestrator
```

### Option 2 — Python module
```
python -m orchestrator.main
```

You should see output like:

```
[metrics-collector] starting...
[java-service] starting...
[node-api] starting...
[orchestrator] 3/3 services running
```

Press **Ctrl+C** to stop everything cleanly.

---

## Configuration

### Default Configuration
The orchestrator currently uses a built‑in default config with placeholder services:

```python
ServiceConfig(
    name="metrics-collector",
    command=["python", "-m", "http.server", "8001"],
)
```

These will be replaced with:

- C++ metrics collector binary  
- Java background service  
- Node.js API gateway  

### Future: External Config File
Support for `config.yaml` and `config.json` is planned.

---

## Code Documentation

The orchestrator includes:

- PEP‑257 docstrings for every class and method  
- Inline comments explaining tricky logic  
- Clear separation between configuration and runtime behavior  

This makes the codebase easy to understand and extend.

---

## Roadmap

- Add health checks  
- Add logging and stdout capture  
- Add restart policies  
- Move service definitions into config.yaml  
- Integrate the real C++ collector  
- Integrate the Java service  
- Integrate the Node API  

---

## Contributing

To run tests:

```
pytest
```

To add a new service:

1. Add a new `ServiceConfig` entry  
2. (Future) Add it to `config.yaml`  
3. Restart the orchestrator  

---

## License
MIT License