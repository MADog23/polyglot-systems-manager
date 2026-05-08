#include "cpu_usage.h"
#include <windows.h>
#include <pdh.h>
#include <pdhmsg.h>
#include <optional>

#pragma comment(lib, "pdh.lib")

static PDH_HQUERY cpuQuery;
static PDH_HCOUNTER cpuTotal;
static bool initialized = false;

std::optional<double> CpuUsage::get_cpu_percent() {
    if (!initialized) {
        if (PdhOpenQuery(NULL, NULL, &cpuQuery) != ERROR_SUCCESS)
            return std::nullopt;

        if (PdhAddCounter(cpuQuery,
            TEXT("\\Processor Information(_Total)\\% Processor Time"),
            NULL,
            &cpuTotal) != ERROR_SUCCESS)
            return std::nullopt;

        // First sample
        if (PdhCollectQueryData(cpuQuery) != ERROR_SUCCESS)
            return std::nullopt;

        initialized = true;
        Sleep(100); // allow time between samples
    }

    if (PdhCollectQueryData(cpuQuery) != ERROR_SUCCESS)
        return std::nullopt;

    PDH_FMT_COUNTERVALUE counterVal;
    if (PdhGetFormattedCounterValue(cpuTotal, PDH_FMT_DOUBLE, NULL, &counterVal) != ERROR_SUCCESS)
        return std::nullopt;

    return counterVal.doubleValue;
}
