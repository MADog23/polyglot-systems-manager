#include "memory_usage.h"

#ifdef _WIN32

#include <windows.h>
#include <optional>
#include <iostream>

/**
 * Windows implementation of memory usage sampling.
 *
 * Uses GlobalMemoryStatusEx to compute:
 *   used = total - available
 *   percent = (used / total) * 100
 */

std::optional<double> MemoryUsage::get_memory_percent() {
    MEMORYSTATUSEX memInfo;
    memInfo.dwLength = sizeof(memInfo);

    if (!GlobalMemoryStatusEx(&memInfo)) {
        std::cerr << "[memory] GlobalMemoryStatusEx failed\n";
        return std::nullopt;
    }

    unsigned long long total = memInfo.ullTotalPhys;
    unsigned long long free  = memInfo.ullAvailPhys;

    if (total == 0) {
        return std::nullopt;
    }

    unsigned long long used = total - free;
    double percent = (static_cast<double>(used) /
                      static_cast<double>(total)) * 100.0;

    return percent;
}

#endif  // _WIN32
