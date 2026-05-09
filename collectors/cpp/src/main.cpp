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

std::atomic<double> smoothedCpu{0.0};
std::atomic<double> smoothedMemory{0.0};
std::atomic<double> smoothedDisk{0.0};

int main() {
    // Background CPU Sampler
    std::thread cpuSampler([]() {
        //std::cout << "[collector] CPU sampler started\n";

        const double alpha = 0.2;

        while (true) {
            auto val = CpuUsage::get_cpu_percent();

            if (val.has_value()) {
                double raw = val.value();                 // extract the double
                latestCpuPercent.store(raw);              // store raw

                double prev = smoothedCpu.load();         // previous smoothed value
                double smooth = alpha * raw + (1.0 - alpha) * prev;

                smoothedCpu.store(smooth);                // store smoothed

                //std::cout << "[collector] CPU raw: " << raw
                //        << " | smooth: " << smooth << "\n";
            } else {
                // PDH sometimes returns no data — this is normal
                // std::cout << "[collector] CPU read failed\n";
            }

            std::this_thread::sleep_for(std::chrono::milliseconds(500));
        }
    });
    cpuSampler.detach();



    // Background Memory Sampler
    std::thread memSampler([]() {
        //std::cout << "[collector] Memory sampler started\n";

        const double alpha = 0.2;

        while (true) {
            auto val = MemoryUsage::get_memory_percent();   // optional<double>

            if (val.has_value()) {
                double raw = val.value();                   // extract double
                latestMemoryPercent.store(raw);

                double prev = smoothedMemory.load();
                double smooth = alpha * raw + (1.0 - alpha) * prev;
                smoothedMemory.store(smooth);

                // Debug:
                // std::cout << "[collector] MEM raw: " << raw
                //           << " | smooth: " << smooth << "\n";
            } else {
                std::cout << "[collector] MEM read failed\n";
            }

            std::this_thread::sleep_for(std::chrono::milliseconds(1000));
        }
    });
    memSampler.detach();




    // Background Uptime Sampler
    std::thread uptimeSampler([]() {
        //std::cout << "[collector] Uptime sampler started\n";

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
        //std::cout << "[collector] Disk sampler started\n";

        const double alpha = 0.2;

        while (true) {
            auto val = DiskUsage::get_disk_percent();       // optional<double>

            if (val.has_value()) {
                double raw = val.value();                   // extract double
                latestDiskPercent.store(raw);

                double prev = smoothedDisk.load();
                double smooth = alpha * raw + (1.0 - alpha) * prev;
                smoothedDisk.store(smooth);

                // Debug:
                // std::cout << "[collector] DISK raw: " << raw
                //           << " | smooth: " << smooth << "\n";
            } else {
                std::cout << "[collector] DISK read failed\n";
            }

            std::this_thread::sleep_for(std::chrono::seconds(2));
        }
    });
    diskSampler.detach();




    httplib::Server svr;

    svr.Get("/metrics", [](const httplib::Request&, httplib::Response& res) {
        res.set_header("Access-Control-Allow-Origin", "*");

        double cpu = smoothedCpu.load();
        double mem = smoothedMemory.load();
        long long uptime = latestUptimeSeconds.load();
        double disk = smoothedDisk.load();

        std::string json =
            "{ \"cpu_percent\": " + std::to_string(cpu) +
            ", \"memory_percent\": " + std::to_string(mem) +
            ", \"uptime_seconds\": " + std::to_string(uptime) +
            ", \"disk_percent\": " + std::to_string(disk) +
            " }";

        res.set_content(json, "application/json");
    });

    svr.Get("/health", [](const httplib::Request&, httplib::Response& res) {
         res.set_header("Access-Control-Allow-Origin", "*");
        res.set_content("OK", "text/plain");
    });




    std::cout << "[metrics-collector] running on http://localhost:9001\n";
    svr.listen("0.0.0.0", 9001);
    return 0;
}
