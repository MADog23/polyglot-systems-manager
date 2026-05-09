#include "uptime.h"
#include <windows.h>
#include <optional>

std::optional<long long> Uptime::get_uptime_seconds() {
    ULONGLONG ms = GetTickCount64();
    return static_cast<long long>(ms / 1000);
}
