#include "metrics.hpp"

#include <string>

/**
 * Convert a Metrics struct into a JSON string.
 *
 * This is used by the /metrics HTTP endpoint in main.cpp.
 * All fields are optional, so missing values become JSON null.
 */

static std::string to_json_optional(const std::optional<double>& v) {
    return v.has_value() ? std::to_string(*v) : "null";
}

static std::string to_json_optional_ll(const std::optional<long long>& v) {
    return v.has_value() ? std::to_string(*v) : "null";
}

std::string metrics_to_json(const Metrics& m) {
    std::string json = "{";
    json += "\"cpu_percent\":" + to_json_optional(m.cpu_percent) + ",";
    json += "\"memory_percent\":" + to_json_optional(m.memory_percent) + ",";
    json += "\"disk_percent\":" + to_json_optional(m.disk_percent) + ",";
    json += "\"uptime_seconds\":" + to_json_optional_ll(m.uptime_seconds);
    json += "}";
    return json;
}
