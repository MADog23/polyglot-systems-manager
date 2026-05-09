# Polyglot Orchestrator

The **Polyglot Orchestrator** is the Python-based control plane for the **Polyglot Systems Manager (PSM)**.  
It is responsible for launching, monitoring, and managing multiple heterogeneous services written in different languages (C++, Java, Node.js, Python), while also serving the system dashboard UI.

This orchestrator acts as a lightweight, educational version of a distributed systems control plane — similar in spirit to systemd, supervisord, or Kubernetes components.

---

## Features

- Launches and supervises multiple services as subprocesses  
- Health checks and restart policies  
- Centralized configuration via `config.yaml`  
- Serves the dashboard UI (`/dashboard`)  
- Proxies metrics from the C++ collector  
- Exposes service health via `/api/services`  
- Clean modular architecture (`core/` + `server/`)  
- CLI entrypoint: `psm-orchestrator`

---

## Architecture

### Directory Structure

```
orchestrator/
│
├── main.py                 # CLI entrypoint
├── pyproject.toml          # Python package definition
│
├── core/                   # Orchestrator control plane
│   ├── orchestrator.py     # Main orchestrator loop
│   ├── service_process.py  # Subprocess wrapper
│   ├── config.py           # YAML loader + config models
│   └── models.py           # Pydantic models
│
└── server/                 # Dashboard + API server
    ├── app.py              # Flask app factory
    └── routes.py           # API endpoints
```

The orchestrator is intentionally split into two subsystems:

- `core/` — pure orchestration logic  
- `server/` — Flask dashboard + API  

This keeps responsibilities clean and maintainable.

---

## How It Works

### 1. Configuration

The orchestrator loads system configuration from:

```
config.yaml
```

This file defines:

- services to launch  
- commands to run  
- health check URLs  
- restart policies  

### 2. Service Management

Each service is represented by a `ServiceProcess` object that handles:

- starting the process  
- checking if it is alive  
- performing health checks  
- restarting if needed  

### 3. Dashboard Server

The Flask server:

- serves the dashboard UI from `/web`  
- proxies metrics from the C++ collector  
- exposes service health via `/api/services`  

The dashboard is available at:

```
http://localhost:8000/dashboard
```

---

## Running the Orchestrator

### 1. Install dependencies

From the `orchestrator/` directory:

```
pip install -e .
```

### 2. Run the orchestrator

```
psm-orchestrator
```

You should see:

```
[orchestrator] loading config from: ../config.yaml
[orchestrator] dashboard available at http://localhost:8000/dashboard
[orchestrator] starting services...
```

---

## Development Notes

- The orchestrator should **not** contain dashboard files — these live in `/web`.  
- Build artifacts (`__pycache__`, `*.egg-info`) should not be committed.  
- The orchestrator is designed to be language‑agnostic — any service that can be started via a command can be managed.  
- The orchestrator runs Flask in a background thread and the control loop in the main thread.

---

## Roadmap

- Log streaming endpoint  
- Multi‑collector support  
- Distributed worker queue  
- Additional dashboard pages  
- WebSocket event streaming  

---

## License

MIT License
