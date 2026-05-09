#include "memory_usage.h"
#include <windows.h>
#include <optional>

std::optional<double> MemoryUsage::get_memory_percent() {
    MEMORYSTATUSEX memInfo;
    memInfo.dwLength = sizeof(memInfo);

    if (!GlobalMemoryStatusEx(&memInfo))
        return std::nullopt;

    DWORDLONG total = memInfo.ullTotalPhys;
    DWORDLONG used  = total - memInfo.ullAvailPhys;

    if (total == 0) return std::nullopt;

    double percent = (double)used / (double)total * 100.0;
    return percent;
}
