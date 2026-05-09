#pragma once

#include <optional>

/**
 * Cross-platform system uptime sampler.
 *
 * Uptime::get_uptime_seconds() returns the number of seconds since the system
 * booted, or std::nullopt if sampling fails.
 *
 * Platform-specific implementations are provided in:
 *   - uptime_windows.cpp
 *   - uptime_linux.cpp
 */
class Uptime {
public:
    /**
     * Returns system uptime in seconds.
     * Returns std::nullopt if sampling fails.
     */
    static std::optional<long long> get_uptime_seconds();
};
