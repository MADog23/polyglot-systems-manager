#pragma once

#include <optional>

/**
 * Cross-platform CPU usage sampler.
 *
 * CpuUsage::get_cpu_percent() returns the current CPU usage as a percentage
 * (0.0–100.0) or std::nullopt if sampling fails.
 *
 * Platform-specific implementations are provided in:
 *   - cpu_usage_windows.cpp
 *   - cpu_usage_linux.cpp
 */
class CpuUsage {
public:
    /**
     * Returns CPU usage as a percentage (0.0–100.0).
     * Returns std::nullopt if sampling fails.
     */
    static std::optional<double> get_cpu_percent();
};
