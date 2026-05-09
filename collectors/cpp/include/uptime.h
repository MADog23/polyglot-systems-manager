#pragma once
#include <optional>

class Uptime {
public:
    // Returns uptime in seconds, or nullopt on error
    static std::optional<long long> get_uptime_seconds();
};
