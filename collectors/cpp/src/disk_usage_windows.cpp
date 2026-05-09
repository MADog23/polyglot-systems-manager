#include "disk_usage.h"
#include <windows.h>
#include <optional>

std::optional<double> DiskUsage::get_disk_percent() {
    ULARGE_INTEGER freeBytesAvailable, totalBytes, freeBytes;

    if (!GetDiskFreeSpaceExW(L"C:\\", &freeBytesAvailable, &totalBytes, &freeBytes))
        return std::nullopt;

    if (totalBytes.QuadPart == 0)
        return std::nullopt;

    double used = (double)(totalBytes.QuadPart - freeBytes.QuadPart);
    double percent = (used / (double)totalBytes.QuadPart) * 100.0;

    return percent;
}
