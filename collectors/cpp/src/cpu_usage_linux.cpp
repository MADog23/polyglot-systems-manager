#include "cpu_usage.h"
#include <fstream>
#include <string>
#include <optional>

static long lastIdle = 0, lastTotal = 0;
static bool initialized = false;

std::optional<double> CpuUsage::get_cpu_percent() {
    std::ifstream file("/proc/stat");
    if (!file.is_open()) return std::nullopt;

    std::string cpu;
    long user, nice, system, idle, iowait, irq, softirq, steal;
    file >> cpu >> user >> nice >> system >> idle >> iowait >> irq >> softirq >> steal;

    long idleTime = idle + iowait;
    long totalTime = user + nice + system + idle + iowait + irq + softirq + steal;

    if (!initialized) {
        lastIdle = idleTime;
        lastTotal = totalTime;
        initialized = true;
        return std::nullopt; // need a second sample
    }

    long diffIdle = idleTime - lastIdle;
    long diffTotal = totalTime - lastTotal;

    lastIdle = idleTime;
    lastTotal = totalTime;

    if (diffTotal == 0) return std::nullopt;

    return 100.0 * (diffTotal - diffIdle) / diffTotal;
}
