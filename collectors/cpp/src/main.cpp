#include <iostream>
#include <atomic>
#include <thread>
#include <chrono>
#include <string>

#include "cpu_usage.h"
#include "memory_usage.h"
#include "uptime.h"
#include "disk_usage.h"
#include "httplib.h"   // existing cpp-httplib library include

static std::atomic<double> latestCpuPercent{0.0};
static std::atomic<double> latestMemoryPercent{0.0};
static std::atomic<long long> latestUptimeSeconds{0};
static std::atomic<double> latestDiskPercent{0.0};

int main() {
    // Background CPU Sampler
    std::thread sampler([]() {
        while (true) {
            auto val = CpuUsage::get_cpu_percent();
            if (val.has_value()) {
                latestCpuPercent.store(val.value());
            }
            std::this_thread::sleep_for(std::chrono::milliseconds(250));
        }
    });
    sampler.detach();

    // Background Memory Sampler
    std::thread memSampler([]() {
        while (true) {
            auto val = MemoryUsage::get_memory_percent();
            if (val.has_value()) {
                latestMemoryPercent.store(val.value());
            }
            std::this_thread::sleep_for(std::chrono::milliseconds(500));
        }
    });
    memSampler.detach();

    // Background Uptime Sampler
    std::thread uptimeSampler([]() {
        while (true) {
            auto val = Uptime::get_uptime_seconds();
            if (val.has_value()) {
                latestUptimeSeconds.store(val.value());
            }
            std::this_thread::sleep_for(std::chrono::seconds(1));
        }
    });
    uptimeSampler.detach();

    // Background Disk Usage Sampler
    std::thread diskSampler([]() {
        while (true) {
            auto val = DiskUsage::get_disk_percent();
            if (val.has_value()) {
                latestDiskPercent.store(val.value());
            }
            std::this_thread::sleep_for(std::chrono::seconds(2));
        }
    });
    diskSampler.detach();

    httplib::Server svr;

    svr.Get("/metrics", [](const httplib::Request&, httplib::Response& res) {
        double cpu = latestCpuPercent.load();
        double mem = latestMemoryPercent.load();
        long long uptime = latestUptimeSeconds.load();
        double disk = latestDiskPercent.load();

        std::string json =
            "{ \"cpu_percent\": " + std::to_string(cpu) +
            ", \"memory_percent\": " + std::to_string(mem) +
            ", \"uptime_seconds\": " + std::to_string(uptime) +
            ", \"disk_percent\": " + std::to_string(disk) +
            " }";

        res.set_content(json, "application/json");
    });

    svr.Get("/health", [](const httplib::Request&, httplib::Response& res) {
        res.set_content("OK", "text/plain");
    });




    std::cout << "[metrics-collector] running on http://localhost:9001\n";
    svr.listen("0.0.0.0", 9001);
    return 0;
}
