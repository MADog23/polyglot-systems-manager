#include <iostream>
#include "httplib.h"
#include "metrics.hpp"

int main() {
    httplib::Server svr;

    // Health endpoint
    svr.Get("/health", [](const httplib::Request&, httplib::Response& res) {
        res.set_content("OK", "text/plain");
    });

    // Metrics endpoint
    svr.Get("/metrics", [](const httplib::Request&, httplib::Response& res) {
        Metrics m = collect_metrics();
        std::string json = metrics_to_json(m);
        res.set_content(json, "application/json");
    });

    std::cout << "[metrics-collector] running on http://localhost:9001\n";

    // Listen on port 9001
    svr.listen("0.0.0.0", 9001);

    return 0;
}
