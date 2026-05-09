#pragma once
#include <optional>

class MemoryUsage {
public:
    // Returns memory usage percentage (0.0–100.0), or nullopt on error
    static std::optional<double> get_memory_percent();
};
