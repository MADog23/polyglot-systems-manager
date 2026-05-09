# C++ Metrics Collector

The C++ Metrics Collector is a lightweight, cross‑platform system metrics service used by the Polyglot Systems Manager. It exposes real‑time CPU, memory, disk, and uptime data through a small embedded HTTP server built on the header‑only `cpp-httplib` library.

The collector runs as an independent process and is supervised by the Python orchestrator. It provides two HTTP endpoints:

- `/health` — returns a simple JSON status used by the orchestrator’s health checks  
- `/metrics` — returns a JSON object containing the latest sampled system metrics

Metrics are gathered by background sampler threads that update a shared `Metrics` struct. Each metric is optional, allowing the collector to operate even when a specific subsystem is unavailable on the host platform.

Platform‑specific implementations are located in the `src` directory and selected automatically by CMake. Windows uses PDH, GlobalMemoryStatusEx, GetDiskFreeSpaceExW, and GetTickCount64. Linux implementations use `/proc` and standard system calls.

The collector is designed to be small, robust, and dependency‑free, making it suitable for embedding in distributed systems, monitoring pipelines, or local development environments.

To build the collector, configure the project with CMake and compile using your preferred toolchain. The resulting executable is named `metrics-collector` and listens on port 9001 by default.
