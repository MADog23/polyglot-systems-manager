#include "uptime.h"

#ifdef _WIN32

#include <windows.h>
#include <optional>
#include <iostream>

/**
 * Windows implementation of system uptime sampling.
 *
 * Uses GetTickCount64(), which returns milliseconds since system boot.
 */

std::optional<long long> Uptime::get_uptime_seconds() {
    ULONGLONG ms = GetTickCount64();

    // Should never be zero unless the system just booted
    if (ms == 0) {
        std::cerr << "[uptime] GetTickCount64 returned 0\n";
        return std::nullopt;
    }

    long long seconds = static_cast<long long>(ms / 1000ULL);
    return seconds;
}

#endif  // _WIN32
