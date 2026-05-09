#pragma once

#include <optional>

/**
 * Cross-platform disk usage sampler.
 *
 * DiskUsage::get_disk_percent() returns the percentage of disk space used
 * (0.0–100.0) or std::nullopt if sampling fails.
 *
 * Platform-specific implementations are provided in:
 *   - disk_usage_windows.cpp
 *   - disk_usage_linux.cpp
 */
class DiskUsage {
public:
    /**
     * Returns disk usage as a percentage (0.0–100.0).
     * Returns std::nullopt if sampling fails.
     */
    static std::optional<double> get_disk_percent();
};
