#include <iostream>
#include <atomic>
#include <thread>
#include <chrono>
#include <string>

#include "cpu_usage.h"
#include "httplib.h"   // your existing cpp-httplib include

static std::atomic<double> latestCpuPercent{0.0};

int main() {
    // Background CPU sampler
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

    httplib::Server svr;

    svr.Get("/health", [](const httplib::Request&, httplib::Response& res) {
        res.set_content("{\"status\":\"ok\"}", "application/json");
    });

    svr.Get("/metrics", [](const httplib::Request&, httplib::Response& res) {
        double cpu = latestCpuPercent.load();
        std::string json = "{ \"cpu_percent\": " + std::to_string(cpu) + " }";
        res.set_content(json, "application/json");
    });

    std::cout << "[metrics-collector] running on http://localhost:9001\n";
    svr.listen("0.0.0.0", 9001);
    return 0;
}
