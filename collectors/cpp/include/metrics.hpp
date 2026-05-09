#pragma once

#include <optional>

/**
 * Aggregated system metrics structure.
 *
 * This struct is populated by the collector's background sampler threads
 * and returned by the /metrics HTTP endpoint.
 *
 * All fields use std::optional so that missing or failed samples
 * do not break the JSON response.
 */
struct Metrics {
    std::optional<double> cpu_percent;      // CPU usage (0.0–100.0)
    std::optional<double> memory_percent;   // RAM usage (0.0–100.0)
    std::optional<double> disk_percent;     // Disk usage (0.0–100.0)
    std::optional<long long> uptime_seconds; // System uptime in seconds
};
