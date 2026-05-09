#include "disk_usage.h"

#ifdef _WIN32

#include <windows.h>
#include <optional>
#include <iostream>

/**
 * Windows implementation of disk usage sampling.
 *
 * Uses GetDiskFreeSpaceExW to compute:
 *   used = total - free
 *   percent = (used / total) * 100
 */

std::optional<double> DiskUsage::get_disk_percent() {
    ULARGE_INTEGER freeBytesAvailable;
    ULARGE_INTEGER totalBytes;
    ULARGE_INTEGER freeBytes;

    BOOL ok = GetDiskFreeSpaceExW(
        L"C:\\",                // root drive
        &freeBytesAvailable,
        &totalBytes,
        &freeBytes
    );

    if (!ok) {
        std::cerr << "[disk] GetDiskFreeSpaceExW failed\n";
        return std::nullopt;
    }

    if (totalBytes.QuadPart == 0) {
        return std::nullopt;
    }

    unsigned long long used = totalBytes.QuadPart - freeBytes.QuadPart;
    double percent = (static_cast<double>(used) /
                      static_cast<double>(totalBytes.QuadPart)) * 100.0;

    return percent;
}

#endif  // _WIN32
