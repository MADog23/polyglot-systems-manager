#pragma once

#include <string>

struct Metrics {
    double cpu_usage;
    double memory_usage;
    double uptime_seconds;
};

Metrics collect_metrics();
std::string metrics_to_json(const Metrics& m);
