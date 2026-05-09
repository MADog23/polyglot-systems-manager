#include <iostream>
#include <thread>
#include <atomic>
#include <chrono>

#include "httplib.h"
#include "metrics.hpp"
#include "cpu_usage.h"
#include "memory_usage.h"
#include "disk_usage.h"
#include "uptime.h"

/**
 * Global metrics instance updated by background sampler threads.
 */
static Metrics g_metrics;

/**
 * Helper: safely update an optional<double> metric.
 */
template <typename Func>
void sample_metric(std::optional<double>& target, Func sampler) {
    auto value = sampler();
    if (value.has_value()) {
        target = value.value();
    }
}

/**
 * Helper: safely update an optional<long long> metric.
 */
template <typename Func>
void sample_metric_ll(std::optional<long long>& target, Func sampler) {
    auto value = sampler();
    if (value.has_value()) {
        target = value.value();
    }
}

/**
 * Background sampler thread for CPU usage.
 */
void cpu_sampler() {
    while (true) {
        sample_metric(g_metrics.cpu_percent, []() {
            return CpuUsage::get_cpu_percent();
        });
        std::this_thread::sleep_for(std::chrono::seconds(1));
    }
}

/**
 * Background sampler thread for memory usage.
 */
void memory_sampler() {
    while (true) {
        sample_metric(g_metrics.memory_percent, []() {
            return MemoryUsage::get_memory_percent();
        });
        std::this_thread::sleep_for(std::chrono::seconds(1));
    }
}

/**
 * Background sampler thread for disk usage.
 */
void disk_sampler() {
    while (true) {
        sample_metric(g_metrics.disk_percent, []() {
            return DiskUsage::get_disk_percent();
        });
        std::this_thread::sleep_for(std::chrono::seconds(5));
    }
}

/**
 * Background sampler thread for uptime.
 */
void uptime_sampler() {
    while (true) {
        sample_metric_ll(g_metrics.uptime_seconds, []() {
            return Uptime::get_uptime_seconds();
        });
        std::this_thread::sleep_for(std::chrono::seconds(1));
    }
}

int main() {
    std::cout << "[collector] starting metrics collector..." << std::endl;

    // Start background sampler threads
    std::thread(cpu_sampler).detach();
    std::thread(memory_sampler).detach();
    std::thread(disk_sampler).detach();
    std::thread(uptime_sampler).detach();

    // Start HTTP server
    httplib::Server server;

    server.Get("/health", [](const httplib::Request&, httplib::Response& res) {
        res.set_content("{\"status\":\"ok\"}", "application/json");
    });

    server.Get("/metrics", [](const httplib::Request&, httplib::Response& res) {
        std::string json = "{";
        json += "\"cpu_percent\":" + (g_metrics.cpu_percent ? std::to_string(*g_metrics.cpu_percent) : "null") + ",";
        json += "\"memory_percent\":" + (g_metrics.memory_percent ? std::to_string(*g_metrics.memory_percent) : "null") + ",";
        json += "\"disk_percent\":" + (g_metrics.disk_percent ? std::to_string(*g_metrics.disk_percent) : "null") + ",";
        json += "\"uptime_seconds\":" + (g_metrics.uptime_seconds ? std::to_string(*g_metrics.uptime_seconds) : "null");
        json += "}";

        res.set_content(json, "application/json");
    });

    std::cout << "[collector] listening on http://localhost:9001" << std::endl;
    server.listen("0.0.0.0", 9001);

    return 0;
}
