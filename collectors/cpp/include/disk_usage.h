#pragma once
#include <optional>

class DiskUsage {
public:
    // Returns disk usage percent (0.0–100.0), or nullopt on error
    static std::optional<double> get_disk_percent();
};
