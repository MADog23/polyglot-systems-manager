#include "uptime.h"
#include <fstream>
#include <optional>

std::optional<long long> Uptime::get_uptime_seconds() {
    std::ifstream file("/proc/uptime");
    if (!file.is_open()) return std::nullopt;

    double uptimeSeconds = 0.0;
    file >> uptimeSeconds;

    return static_cast<long long>(uptimeSeconds);
}
