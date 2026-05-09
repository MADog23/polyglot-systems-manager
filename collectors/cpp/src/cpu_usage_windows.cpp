#include "cpu_usage.h"

#ifdef _WIN32

#include <windows.h>
#include <pdh.h>
#include <pdhmsg.h>
#include <optional>
#include <iostream>

#pragma comment(lib, "pdh.lib")

/**
 * Windows implementation using PDH (Performance Data Helper).
 *
 * CPU usage is sampled by querying the "\Processor(_Total)\% Processor Time"
 * performance counter. Two samples are required for a valid reading.
 */

static bool initialized = false;
static PDH_HQUERY cpuQuery;
static PDH_HCOUNTER cpuTotal;

std::optional<double> CpuUsage::get_cpu_percent() {
    if (!initialized) {
        if (PdhOpenQuery(NULL, 0, &cpuQuery) != ERROR_SUCCESS) {
            std::cerr << "[cpu] PdhOpenQuery failed\n";
            return std::nullopt;
        }

        if (PdhAddCounter(cpuQuery, TEXT("\\Processor(_Total)\\% Processor Time"),
                          0, &cpuTotal) != ERROR_SUCCESS) {
            std::cerr << "[cpu] PdhAddCounter failed\n";
            return std::nullopt;
        }

        if (PdhCollectQueryData(cpuQuery) != ERROR_SUCCESS) {
            std::cerr << "[cpu] PdhCollectQueryData (initial) failed\n";
            return std::nullopt;
        }

        initialized = true;
        return std::nullopt;  // first sample is always invalid
    }

    if (PdhCollectQueryData(cpuQuery) != ERROR_SUCCESS) {
        std::cerr << "[cpu] PdhCollectQueryData failed\n";
        return std::nullopt;
    }

    PDH_FMT_COUNTERVALUE counterVal;
    if (PdhGetFormattedCounterValue(cpuTotal, PDH_FMT_DOUBLE, NULL, &counterVal)
        != ERROR_SUCCESS) {
        std::cerr << "[cpu] PdhGetFormattedCounterValue failed\n";
        return std::nullopt;
    }

    return counterVal.doubleValue;
}

#endif  // _WIN32
