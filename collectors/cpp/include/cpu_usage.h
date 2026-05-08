#pragma once
#include <optional>

class CpuUsage {
public:
    // Returns CPU usage as a percentage (0.0–100.0), or std::nullopt on error
    static std::optional<double> get_cpu_percent();
};
