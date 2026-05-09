#pragma once

#include <optional>

/**
 * Cross-platform memory usage sampler.
 *
 * MemoryUsage::get_memory_percent() returns the percentage of RAM used
 * (0.0–100.0) or std::nullopt if sampling fails.
 *
 * Platform-specific implementations are provided in:
 *   - memory_usage_windows.cpp
 *   - memory_usage_linux.cpp
 */
class MemoryUsage {
public:
    /**
     * Returns memory usage as a percentage (0.0–100.0).
     * Returns std::nullopt if sampling fails.
     */
    static std::optional<double> get_memory_percent();
};
