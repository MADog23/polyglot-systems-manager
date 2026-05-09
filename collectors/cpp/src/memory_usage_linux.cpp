#include "memory_usage.h"
#include <fstream>
#include <string>
#include <optional>

std::optional<double> MemoryUsage::get_memory_percent() {
    std::ifstream file("/proc/meminfo");
    if (!file.is_open()) return std::nullopt;

    long memTotal = 0, memAvailable = 0;
    std::string key;
    long value;
    std::string unit;

    while (file >> key >> value >> unit) {
        if (key == "MemTotal:") memTotal = value;
        if (key == "MemAvailable:") memAvailable = value;
        if (memTotal && memAvailable) break;
    }

    if (memTotal == 0) return std::nullopt;

    long used = memTotal - memAvailable;
    double percent = (double)used / (double)memTotal * 100.0;

    return percent;
}
