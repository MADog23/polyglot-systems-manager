#include "metrics.hpp"
#include <chrono>

Metrics collect_metrics() {
    static auto start = std::chrono::steady_clock::now();

    Metrics m;
    m.cpu_usage = 0.0;        // TODO: real CPU usage
    m.memory_usage = 0.0;     // TODO: real memory usage

    auto now = std::chrono::steady_clock::now();
    m.uptime_seconds = std::chrono::duration<double>(now - start).count();

    return m;
}

std::string metrics_to_json(const Metrics& m) {
    return "{"
           "\"cpu_usage\": " + std::to_string(m.cpu_usage) + ", "
           "\"memory_usage\": " + std::to_string(m.memory_usage) + ", "
           "\"uptime_seconds\": " + std::to_string(m.uptime_seconds) +
           "}";
}
